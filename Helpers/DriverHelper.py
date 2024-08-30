import time
from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class DriverHelper:
    def __init__(self, start_url=''):
        self.driver = self._get_driver(start_url)

    def scroll_element_height(self, css_selector):
        element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', element)

    def get(self, url: str, random_sleep=False):
        self.driver.get(url)
        if random_sleep:
            time.sleep(randint(2, 3))

    def close(self):
        self.driver.quit()

    @staticmethod
    def _get_driver(start_url='') -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless=new')
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=chrome_options)
        if start_url:
            driver.get(start_url)
        return driver
