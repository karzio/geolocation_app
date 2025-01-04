from geolocation_service.api_client import ApiClient


class Service:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def retrieve(self, web_address: str) -> dict:
        return self.api_client.retrieve_geolocation_data(web_address)
