from rest_framework import serializers
from .models import MetaHotel, Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'
    
class MetaHotelSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True)
    
    class Meta:
        model = MetaHotel
        fields = '__all__'