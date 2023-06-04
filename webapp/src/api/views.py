from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import HotelSerializer
from .models import MetaHotel, Hotel


class HotelViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
        | Создать отель поставщика
        | Перепривязать отель к другому мета-отелю
    """
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

