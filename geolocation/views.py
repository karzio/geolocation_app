from rest_framework import mixins, viewsets

from geolocation.models import GeoLocation
from geolocation.serializers import (
    GeoLocationCreateSerializer,
    GeoLocationListSerializer,
    GeoLocationSerializer,
)


class GeoLocationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = GeoLocation.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return GeoLocationCreateSerializer
        elif self.action == "list":
            return GeoLocationListSerializer
        return GeoLocationSerializer
