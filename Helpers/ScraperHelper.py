import datetime
import re
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from Helpers.ApiHelper import ApiHelper
from Helpers.Bs4Helper import Bs4Helper
from Helpers.DriverHelper import DriverHelper
from Models.DataRequestModel import DataRequestModel


class ScraperHelper:
    def __init__(self):
        self._base_url = 'https://www.land.com/Texas/all-land/over-10-acres/is-active/is-under-contract/'
        self._driver_helper = DriverHelper(self._base_url)
        self._bs4_helper = Bs4Helper(self._driver_helper)
        self._api_helper = ApiHelper()

    def start_scraper(self):
        pages = self._get_pages()
        for page_index, page in enumerate(pages):
            print(f'On page {page_index + 1} of {len(pages) + 1}')
            self._driver_helper.get(page, random_sleep=False)
            listings = self._scrape_listings()
            print(f'Saving {len(listings)} lands...')
            self._api_helper.save_many_lands(listings)
            print('Lands saved successfully')
        print('Scraper Ran successfully!')
        self._driver_helper.close()

    def _get_pages(self) -> list[str]:
        self._driver_helper.scroll_element_height('div.a671b._7d19a')
        time.sleep(5)
        soup = self._bs4_helper.get_soup()
        total_pages = int(soup.select_one('div._95b7d span.cc74c:last-child').text)
        all_pages = [f'{self._base_url}page-{i}' for i in range(1, total_pages + 1)]
        return all_pages

    def _get_listings(self) -> list[str]:
        soup = self._bs4_helper.get_soup()
        listings_on_page = soup.select('div[data-testid=placards] div#placard-container div._3906 a, div._196cf a')
        return [urljoin(self._base_url, listing.get('href')) for listing in listings_on_page]

    def _scrape_listings(self) -> list:
        listings = self._get_listings()
        listing_models = []
        for listing_index, listing in enumerate(listings):
            print(f'On listing {listing_index + 1} of {len(listings) + 1}')
            self._driver_helper.get(listing, random_sleep=False)
            listing_model = self._scrape_listing(listing)
            listing_models.append(listing_model.model_dump())
        return listing_models

    def _scrape_listing(self, listing: str) -> DataRequestModel:
        soup = self._bs4_helper.get_soup()
        price, acres = self._get_price_and_acres(soup)
        area, beds, baths, half_baths = self._get_bed_bath_area(soup)
        property_status = self._get_property_status(soup)
        county = self._get_county(soup)
        description = self._get_description(soup)
        electricity, water_front, mineral, well, ag_exempt = self._get_facilities(description)
        created_at = datetime.datetime.now(datetime.UTC)
        return DataRequestModel(
            county=county,
            origin='Lands of Texas',
            createdAt=created_at.isoformat(),
            createdAtMonth=created_at.month,
            createdAtYear=created_at.year,
            status=property_status,
            price=price,
            pricePerAcre=round(price / acres) if price else 0.0,
            area=area,
            acre=acres,
            bedrooms=beds,
            bathrooms=baths + half_baths,
            electricity=electricity,
            waterfront=water_front,
            mineral=mineral,
            well=well,
            agExempt=ag_exempt,
            link=listing
        )

    @staticmethod
    def _get_facilities(description: str) -> [bool, bool, bool, bool, bool]:
        electricity = 'electricity' in description
        water_front = 'water front' in description
        mineral = 'mineral' in description
        well = 'well' in description
        ag_exempt = 'ag exempt' in description
        return electricity, water_front, mineral, well, ag_exempt

    @staticmethod
    def _get_description(soup: BeautifulSoup):
        description_land, secondary_detail = '', ''
        if description_land_container := soup.select_one('div[data-testid=DescriptionLand]'):
            description_land = description_land_container.get_text(' ', strip=True).lower()
        if secondary_detail_container := soup.select_one('div[data-testid=SecondaryDetails]'):
            secondary_detail = secondary_detail_container.get_text(' ', strip=True).lower()
        return f'{description_land} {secondary_detail}'

    @staticmethod
    def _get_county(soup: BeautifulSoup) -> str:
        if county_container := soup.select_one('div._0e55d'):
            county_container_str = county_container.get_text(' ', strip=True)
            if match := re.search(r'-\s([\w\s]+)\sCounty', county_container_str):
                return match.group(1)
        return ''

    @staticmethod
    def _get_property_status(soup: BeautifulSoup) -> str:
        if property_status_container := soup.select_one('div._2d4dc'):
            return property_status_container.text
        return ''

    @staticmethod
    def _get_bed_bath_area(soup: BeautifulSoup) -> [float, float, float, float]:
        area, beds, baths, half_baths = 0.0, 0, 0, 0
        if property_area_details_container := soup.select_one('div._43054'):
            property_area_details = property_area_details_container.get_text(' ', strip=True)
            if beds_match := re.search(r'(\d+)\s+beds', property_area_details):
                beds = int(beds_match.group(1)) if beds_match else 0
            if baths_match := re.search(r'(\d+)\s+baths', property_area_details):
                baths = int(baths_match.group(1)) if baths_match else 0
            if half_baths_match := re.search(r'(\d+)\s+half\s+baths', property_area_details):
                half_baths = int(half_baths_match.group(1)) if half_baths_match else 0
            if area_match := re.search(r'([\d,]+)\s+sq\s+ft', property_area_details):
                area = float(area_match.group(1).replace(',', '')) if area_match else 0.0
        return area, beds, baths, half_baths

    @staticmethod
    def _get_price_and_acres(soup: BeautifulSoup) -> [float, float]:
        price, acres = 0.0, 0.0
        if property_info_container := soup.select_one('div._1e694'):
            property_info = property_info_container.get_text(' ', strip=True)
            if price_match := re.search(r'\$([\d,]+)', property_info):
                price = float(price_match.group(1).replace(',', ''))
            if acres_match := re.search(r'(\d[\d,]*)\s+Acres', property_info):
                acres = float(acres_match.group(1).replace(',', ''))
        return price, acres
