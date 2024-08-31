from urllib.parse import urljoin

import requests


class ApiHelper:
    def __init__(self):
        self._base_url = 'http://localhost:5217/api/'

    def save_many_lands(self, lands: list):
        url = urljoin(self._base_url, 'Land/SaveLands')
        response = requests.post(url, json=lands, verify=False)
        response.raise_for_status()
