from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MetaHotelViewSet, HotelViewSet, BindHotelsAPIView


router = DefaultRouter()
router.register('hotel', HotelViewSet, basename='hotel')
router.register('metahotel', MetaHotelViewSet, basename='metahotel')


urlpatterns = [
    path('bind/', BindHotelsAPIView.as_view(), name='bind-hotels')
] + router.urls