from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geolocation.geolocation_service.tests.fixtures import request_get_mock
from geolocation.models import GeoLocation


class TestGeoLocationViewSet(APITestCase):
    def setUp(self):
        self.geolocation_data = {"web_address": "http://example.com"}
        self.geolocation = GeoLocation.objects.create(
            latitude=40.7589111328125,
            longitude=-73.97901916503906,
            country="United States",
            city="Manhattan",
            zip="10020",
            web_address="http://example2.com",
        )
        self.create_url = reverse("geolocation-list")
        self.detail_url = reverse(
            "geolocation-detail", kwargs={"pk": self.geolocation.pk}
        )

    def tearDown(self):
        GeoLocation.objects.all().delete()

    @patch("requests.get", return_value=request_get_mock())
    def test_create_geolocation(self, requests_get_mock):
        response = self.client.post(
            self.create_url, self.geolocation_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GeoLocation.objects.count(), 2)

    def test_create_geolocation_invalid_web_address_fails(self):
        response = self.client.post(
            self.create_url, {"web_address": "invalid"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(GeoLocation.objects.count(), 1)

    def test_create_geolocation_missing_web_address_fails(self):
        response = self.client.post(self.create_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(GeoLocation.objects.count(), 1)

    def test_list_geolocations(self):
        response = self.client.get(self.create_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_geolocation(self):
        response = self.client.get(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], self.geolocation.city)

    def test_get_geolocation_not_found(self):
        response = self.client.get(
            reverse("geolocation-detail", kwargs={"pk": 2}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_geolocation(self):
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GeoLocation.objects.count(), 0)

    def test_delete_geolocation_not_found(self):
        response = self.client.delete(
            reverse("geolocation-detail", kwargs={"pk": 2}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(GeoLocation.objects.count(), 1)
