import os

import requests

from geolocation.geolocation_service.exceptions import (
    ExternalAPIError,
    ResourceNotFoundError,
)


class IPStackApiClient:
    """
    API Client to retrieve geolocation data from IP Stack API.
    https://ipstack.com/documentation
    """

    def __init__(self):
        self.api_key = os.environ.get("IP_STACK_API_KEY")
        self.url = "https://api.ipstack.com/{}?access_key={}"

    def retrieve_geolocation_data(self, web_address: str) -> dict:
        url = self.url.format(web_address, self.api_key)
        response = requests.get(url)

        # Something went wrong with IP stack server, because typically IP Stack returns status code 200
        # even if the web address is not found or the API key is invalid.
        if response.status_code != 200:
            raise ExternalAPIError("Unexpected error occurred")

        json_data = response.json()

        if json_data.get("success") is False:
            if json_data.get("error", {}).get("code") == 404:
                raise ResourceNotFoundError()
            else:
                raise ExternalAPIError("Unexpected error occurred")

        geolocation_data = {
            "latitude": json_data.get("latitude"),
            "longitude": json_data.get("longitude"),
            "country": json_data.get("country_name"),
            "city": json_data.get("city"),
            "zip": json_data.get("zip"),
        }
        return geolocation_data
