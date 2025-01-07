from unittest import TestCase
from unittest.mock import patch

from geolocation.geolocation_service.api_client import IPStackApiClient
from geolocation.geolocation_service.exceptions import (
    ExternalAPIError,
    ResourceNotFoundError,
)
from geolocation.geolocation_service.tests.fixtures import (
    request_get_mock,
    request_get_mock_not_found,
    request_get_mock_success_false,
)


class TestAPIClient(TestCase):
    @patch("requests.get", return_value=request_get_mock())
    def test_status_code_not_equal_200_raises_error(self, requests_get_mock):
        requests_get_mock.return_value.status_code = 500
        with self.assertRaises(ExternalAPIError):
            IPStackApiClient().retrieve_geolocation_data("example.com")

    @patch("requests.get", return_value=request_get_mock_success_false())
    def test_success_false_raises_error(self, requests_get_mock):
        with self.assertRaises(ExternalAPIError):
            IPStackApiClient().retrieve_geolocation_data("example.com")

    @patch("requests.get", return_value=request_get_mock_not_found())
    def test_not_found_raises_error(self, requests_get_mock):
        with self.assertRaises(ResourceNotFoundError):
            IPStackApiClient().retrieve_geolocation_data("example.com")
