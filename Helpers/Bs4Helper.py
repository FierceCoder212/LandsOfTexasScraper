from bs4 import BeautifulSoup

from Helpers.DriverHelper import DriverHelper


class Bs4Helper:
    def __init__(self, driver_helper: DriverHelper):
        self._driver_helper = driver_helper

    def get_soup(self):
        return BeautifulSoup(self._driver_helper.driver.page_source, 'html.parser')

    def set_driver(self, driver_helper: DriverHelper):
        self._driver_helper = driver_helper
