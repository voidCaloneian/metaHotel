from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db import transaction
from .serializers import MetaHotelSerializer, HotelSerializer, HotelHistorySerializer
from .models import MetaHotel, Hotel


HOTEL_HISTORY_SERIALIZER = HotelHistorySerializer
META_HOTEL_SERIALIZER = MetaHotelSerializer
HOTEL_SERIALIZER = HotelSerializer

class HotelViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """
        | Создать отель поставщика
        | Перепривязать отель к другому мета-отелю
    """
    serializer_class = HOTEL_SERIALIZER
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
    serializer_class = META_HOTEL_SERIALIZER
    queryset = MetaHotel.objects.prefetch_related('hotels').all()
    
class BindHotelsAPIView(APIView):
    """
        | Объединить 1 и более отелей поставщиков в один мета-отель
    """
    meta_hotel_serializer = META_HOTEL_SERIALIZER
    def put(self, request, *args, **kwargs):
        hotel_pks = request.data.get('hotels_pks').split(',')
        meta_hotel_id = request.data.get('meta_hotel', None)
        
        meta_hotel = MetaHotel.objects.get_or_create(id=meta_hotel_id)[0]
        hotels = Hotel.objects.filter(pk__in=hotel_pks)
        
        self.update_meta_hotel_and_save_history(hotels, meta_hotel)
        
        serializer = self.meta_hotel_serializer(meta_hotel)
        
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