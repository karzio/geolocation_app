from django.db import models


class GeoLocation(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    web_address = models.CharField(
        max_length=255,
        unique=True,
        help_text="Web address or IP address. "
        "Start with a protocol (http:// or https://)",
    )

    def __str__(self):
        return (
            f"Host: {self.web_address} is from {self.country}, {self.city}, {self.zip}"
        )

    def __repr__(self):
        return f"GeoLocation(web_address={self.web_address}, latitude={self.latitude}, longitude={self.longitude}, city='{self.city}', country='{self.country}')"
