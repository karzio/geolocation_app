from unittest.mock import patch

from django.core import exceptions
from django.db import transaction
from django.test import TestCase
from parameterized import parameterized
from rest_framework.exceptions import APIException, ValidationError

from geolocation.geolocation_service.tests.fixtures import (
    request_get_mock,
    request_get_mock_missing_fields,
    request_get_mock_not_found,
    request_get_mock_success_false,
)
from geolocation.models import GeoLocation
from geolocation.serializers import GeoLocationCreateSerializer


class TestGeoLocationCreateSerializer(TestCase):
    def setUp(self):
        self.data = {
            "id": 1,
            "latitude": 40.7589111328125,
            "longitude": -73.97901916503906,
            "country": "United States",
            "city": "Manhattan",
            "zip": "10020",
            "web_address": "http://example.com",
        }
        self.data2 = {
            "id": 2,
            "latitude": 40.7589111328125,
            "longitude": -73.97901916503906,
            "country": "United States",
            "city": "Manhattan",
            "zip": "10020",
            "web_address": "example2.com",
        }
        self.geolocation = GeoLocation.objects.create(**self.data2)
        self.data2["web_address"] = "http://example2.com"

    def tearDown(self):
        GeoLocation.objects.all().delete()

    @patch("requests.get", return_value=request_get_mock())
    def test_create_valid(self, mock_requests_get):
        serializer = GeoLocationCreateSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(GeoLocation.objects.count(), 2)

    @patch("requests.get", return_value=request_get_mock_missing_fields())
    def test_create_with_missing_fields_from_api(self, requests_get_mock):
        serializer = GeoLocationCreateSerializer(
            data={"web_address": "http://example.com"}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(GeoLocation.objects.count(), 2)

    def test_create_invalid_web_address_fails(self):
        serializer = GeoLocationCreateSerializer(data={"web_address": "invalid"})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
        self.assertEqual(GeoLocation.objects.count(), 1)

    @patch("requests.get", return_value=request_get_mock_success_false())
    def test_create_catches_external_api_error(self, requests_get_mock):
        serializer = GeoLocationCreateSerializer(
            data={"web_address": "http://example.com"}
        )
        with self.assertRaises(APIException):
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
        self.assertEqual(GeoLocation.objects.count(), 1)

    @patch("requests.get", return_value=request_get_mock_not_found())
    def test_create_catches_not_found_error(self, requests_get_mock):
        serializer = GeoLocationCreateSerializer(
            data={"web_address": "http://example.com"}
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
        self.assertEqual(GeoLocation.objects.count(), 1)

    def test_create_duplicate_fails(self):
        serializer = GeoLocationCreateSerializer(data=self.data2)
        with self.assertRaises(ValidationError):
            serializer.validate_web_address(self.data2["web_address"])
        self.assertEqual(GeoLocation.objects.count(), 1)

    @patch("requests.get", return_value=request_get_mock())
    def test_integrity_error_is_caught(self, requests_get_mock):
        serializer = GeoLocationCreateSerializer(data=self.data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data.copy()
            validated_data["web_address"] = "example2.com"
            with transaction.atomic():
                serializer.create(validated_data)

    @parameterized.expand(
        [
            ("http://www.example.com", "example.com"),
            ("https://www.example.com", "example.com"),
            ("http://example.com", "example.com"),
            ("https://example.com", "example.com"),
            ("http://www.example.com/", "example.com"),
            ("http://www.example.com/?q=1", "example.com"),
            ("http://www.example.com?q=1", "example.com"),
            ("http://www.examplewww.com", "examplewww.com"),
            (
                "https://[2001:dd8:3333:4444:5555:6666:7777:8888]",
                "[2001:dd8:3333:4444:5555:6666:7777:8888]",
            ),
            ("https://93.184.215.14", "93.184.215.14"),
        ]
    )
    def test_normalize_web_address(self, input_url, expected_output):
        self.assertEqual(
            GeoLocationCreateSerializer.normalize_web_address(input_url),
            expected_output,
        )
