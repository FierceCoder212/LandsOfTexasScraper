import time
from random import randint

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By


class DriverHelper:
    def __init__(self, start_url=''):
        self.driver = self._get_driver(start_url)

    def scroll_element_height(self, css_selector):
        element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', element)

    def get(self, url: str, random_sleep=False):
        while True:
            try:
                self.driver.get(url)
                break
            except TimeoutException:
                self.driver.quit()
                self.driver = self._get_driver(url)
        if random_sleep:
            time.sleep(randint(2, 3))

    def close(self):
        self.driver.quit()

    @staticmethod
    def _get_driver(start_url='') -> WebDriver:
        firefox_options = Options()
        # firefox_options.set_preference('javascript.enabled', False)
        firefox_options.set_preference('permissions.default.image', 2)
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--start-maximized')
        
        driver = webdriver.Firefox(options=firefox_options)
        if start_url:
            driver.get(start_url)
        return driver
