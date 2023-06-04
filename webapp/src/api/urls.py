from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet


router = DefaultRouter()
router.register('hotel', HotelViewSet, basename='hotel')


urlpatterns = [
] + router.urls