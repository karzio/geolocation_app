import requests


class ApiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.ipstack.com/{}?api_key={}"

    def retrieve_geolocation_data(self, web_address: str) -> dict:
        response = requests.get(self.url.format(web_address, self.api_key))

        return response.json()
