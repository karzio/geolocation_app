from rest_framework import serializers

from geolocation.models import GeoLocation


class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = ["web_address", "name"]

    def create(self, validated_data):
        return GeoLocation.objects.create(**validated_data)
