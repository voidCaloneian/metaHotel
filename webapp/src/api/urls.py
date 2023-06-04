from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MetaHotelViewSet, HotelViewSet


router = DefaultRouter()
router.register('hotel', HotelViewSet, basename='hotel')
router.register('meta-hotel', MetaHotelViewSet, basename='meta-hotel')


urlpatterns = [
] + router.urls