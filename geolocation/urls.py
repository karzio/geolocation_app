from rest_framework.routers import DefaultRouter

from geolocation.views import GeoLocationViewSet

router = DefaultRouter()

router.register("geolocation", GeoLocationViewSet)

geolocation_urlpatterns = router.urls
