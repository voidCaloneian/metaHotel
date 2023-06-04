from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .serializers import MetaHotelSerializer, HotelSerializer, HotelHistorySerializer
from .models import MetaHotel, Hotel


HOTEL_HISTORY_SERIALIZER = HotelHistorySerializer

class HotelViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
        | Создать отель поставщика
        | Перепривязать отель к другому мета-отелю
    """
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        """
            | Получить историю привязки отеля (к каким мета-отелям в какой момент времени он был привязан)
        """
        hotel = self.get_object()
        hotel_serializer = self.get_serializer(hotel)
        
        hotel_data = hotel_serializer.data
        hotel_history_data = HOTEL_HISTORY_SERIALIZER(self.get_hotel_history(hotel), many=True).data
        
        response_data = {
            **hotel_data,
            'history': hotel_history_data
        }
    
        return Response(response_data)
    
    @staticmethod
    def get_hotel_history(hotel):
        return hotel.history.all()
        

class MetaHotelViewSet(ListModelMixin, GenericViewSet):
    """
        | Получить список мета-отелей и входящих в них отелей
    """
    serializer_class = MetaHotelSerializer
    queryset = MetaHotel.objects.prefetch_related('hotels').all()