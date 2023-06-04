from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import HotelSerializer
from .models import MetaHotel, Hotel


class HotelViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = HotelSerializer

