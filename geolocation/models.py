from django.db import models


class GeoLocation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    web_address = models.CharField(max_length=255)
