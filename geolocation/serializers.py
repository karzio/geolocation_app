from django.core.validators import URLValidator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import APIException, ValidationError

from geolocation.geolocation_service import GeoLocationService
from geolocation.geolocation_service.exceptions import (
    ExternalAPIError,
    ResourceNotFoundError,
)
from geolocation.models import GeoLocation


class GeoLocationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating GeoLocation object based on a web_address field.
    Normalizes the web address to prevent duplicates.
    """

    class Meta:
        model = GeoLocation
        fields = "__all__"
        read_only_fields = ("id", "latitude", "longitude", "country", "city", "zip")

    def validate_web_address(self, web_address):
        """
        Validates the web address field to check if it's a correct IP or a web address.
        """
        validator = URLValidator()
        validator(web_address)
        normalized_web_address = self.normalize_web_address(web_address)

        # Check for web address uniqueness based on normalized web address.
        if GeoLocation.objects.filter(web_address=normalized_web_address).exists():
            raise ValidationError("This web address is already in the database")
        return normalized_web_address

    @staticmethod
    def normalize_web_address(web_address):
        """
        Normalizes the web address to prevent duplicates.
        If not, normalize the address.
        """
        normalized_web_address = (
            web_address.replace("http://", "")
            .replace("https://", "")
            .split("/")[0]
            .split("?")[0]
        )
        # Conditional statement for an unlikely case when 'www.' would be in the middle of a web address.
        if normalized_web_address.startswith("www."):
            normalized_web_address = normalized_web_address.replace("www.", "", 1)
        return normalized_web_address

    def create(self, validated_data):
        """
        Creates GeoLocation object if the data is successfully retrieved from an external API
        based on the web_address field that is passed by a user.
        """
        service = GeoLocationService()

        try:
            geo_data = service.retrieve(validated_data["web_address"])
        except ExternalAPIError:
            raise APIException("External API error occurred. Please try again later.")
        except ResourceNotFoundError:
            raise ValidationError("Web address not found")

        validated_data.update(geo_data)

        try:
            instance = GeoLocation.objects.create(**validated_data)
        except IntegrityError as e:
            raise ValidationError(
                "Database integrity error occurred. Please try again later."
            )

        return instance


class GeoLocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = ["id", "web_address"]


class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = "__all__"
