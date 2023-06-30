from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from django.db import transaction

from .serializers import MetaHotelSerializer, HotelSerializer, HotelHistorySerializer
from .models import MetaHotel, Hotel


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
        HotelSerializer = self.get_serializer(hotel)
        
        hotel_data = HotelSerializer.data
        hotel_history_data = HotelHistorySerializer(self.get_hotel_history(hotel), many=True).data
        
        response_data = {
            **hotel_data,
            'history': hotel_history_data
        }
    
        return Response(response_data)
    
    @staticmethod
    def get_hotel_history(hotel):
        return hotel.history.all()
        

class MetaHotelViewSet(ListAPIView):
    """
        | Получить список мета-отелей и входящих в них отелей
    """
    serializer_class = MetaHotelSerializer
    queryset = MetaHotel.objects.prefetch_related('hotels').all()
    
class BindHotelsAPIView(APIView):
    """
        | Объединить 1 и более отелей поставщиков в один мета-отель
    """
    MetaHotelSerializer = MetaHotelSerializer
    def put(self, request, *args, **kwargs):
        hotel_pks = request.data.get('hotels_pks').split(',')
        meta_hotel_id = request.data.get('meta_hotel', None)
        
        meta_hotel = MetaHotel.objects.get_or_create(id=meta_hotel_id)[0]
        hotels = Hotel.objects.select_for_update().filter(pk__in=hotel_pks)
        
        self.update_meta_hotel_and_save_history(hotels, meta_hotel)
        
        serializer = self.MetaHotelSerializer(meta_hotel)
        
        return Response(serializer.data)
    
    @staticmethod
    @transaction.atomic()
    def update_meta_hotel_and_save_history(hotels, meta_hotel):
        #  Обновление было не через update метод для того,
        #  чтобы записывалась и история отелей 
        for hotel in hotels:
            if hotel.meta_hotel != meta_hotel:
                hotel.meta_hotel = meta_hotel
                hotel.save() 
