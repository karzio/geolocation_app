from unittest import TestCase

from geolocation.models import GeoLocation


class TestGeoLocationModel(TestCase):
    """
    Test the GeoLocation model's __str__ and __repr__ methods.
    """

    def setUp(self):
        self.instance = GeoLocation.objects.create(
            latitude=40.7589111328125,
            longitude=-73.97901916503906,
            country="United States",
            city="Manhattan",
            zip="10020",
            web_address="http://example.com",
        )
        self.instance2 = GeoLocation.objects.create(
            latitude=None,
            longitude=None,
            country="United States",
            city="",
            zip="10020",
            web_address="http://example2.com",
        )
        pass

    def tearDown(self):
        GeoLocation.objects.all().delete()

    def test_str(self):
        self.assertEqual(
            str(self.instance),
            "Host: http://example.com is from United States, Manhattan, 10020",
        )

    def test_repr(self):
        with self.subTest("When latitude and longitude are None"):
            self.assertEqual(
                repr(self.instance2),
                "GeoLocation(web_address=http://example2.com, latitude=None, longitude=None, city='', country='United States')",
            )
        with self.subTest("When latitude and longitude are not None"):
            self.assertEqual(
                repr(self.instance),
                "GeoLocation(web_address=http://example.com, latitude=40.7589111328125, longitude=-73.97901916503906, city='Manhattan', country='United States')",
            )
