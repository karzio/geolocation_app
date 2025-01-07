from geolocation.geolocation_service.api_client import IPStackApiClient


class GeoLocationService:
    """
    Geolocation service that instantiates an API client and manages it.
    """

    def __init__(self):
        self.api_client = IPStackApiClient()

    def retrieve(self, web_address: str) -> dict:
        return self.api_client.retrieve_geolocation_data(web_address)
