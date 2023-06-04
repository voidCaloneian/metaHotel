from django.db import models
from django.core.validators import MinLengthValidator


class MetaHotel(models.Model):
    id = models.CharField(primary_key=True, max_length=100, validators=[MinLengthValidator(1)])

    def __str__(self):
        return self.id

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    meta_hotel = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, blank=True, max_length=100, related_name='hotels')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            self.create_hotel_history_if_need(self)
            super().save(*args, **kwargs)
        except Hotel.DoesNotExist:
            super().save(*args, **kwargs)
            HotelHistory.create_hotel_history(self)
    
    @staticmethod
    def create_hotel_history_if_need(instance):
        print("ВЫЗЫВАЛИ?")
        old_hotel_data = Hotel.objects.get(pk=instance.pk)
        old_hotel_meta_hotel = old_hotel_data.meta_hotel
        if old_hotel_meta_hotel != instance.meta_hotel:
            HotelHistory.create_hotel_history(instance)
        

class HotelHistory(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, related_name='history')
    meta_hotel = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, related_name='history')
    linked_datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.hotel} linked to {self.meta_hotel}'
    
    @staticmethod
    def create_hotel_history(instance):
        HotelHistory.objects.create(
            hotel=instance,
            meta_hotel=instance.meta_hotel
        )