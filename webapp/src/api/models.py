from django.db import models, transaction
from django.db.models.signals import post_delete, pre_save
from django.core.validators import MinLengthValidator
from django.dispatch import receiver

class MetaHotel(models.Model):
    id = models.CharField(primary_key=True, max_length=100, validators=[MinLengthValidator(1)])

    def __str__(self):
        return self.id

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    meta_hotel = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, blank=True, max_length=100, related_name='hotels')
    
    def __str__(self):
        return self.name
    
    @transaction.atomic()
    def save(self, *args, **kwargs):
        try:
            self.create_hotel_history_if_need(self)
            super().save(*args, **kwargs)
        except Hotel.DoesNotExist:
            super().save(*args, **kwargs)
            HotelHistory.create_hotel_history(self)
    
    @staticmethod
    def create_hotel_history_if_need(instance):
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
        
#  Переделать сохранение истории на систему сигналов

@receiver(post_delete, sender=Hotel)
def post_delete_hotel(sender ,instance, **kwargs):
    meta_hotel = instance.meta_hotel
    delete_meta_hotel_if_no_hotels(meta_hotel)

@receiver(pre_save, sender=Hotel)
def pre_save_hotel(sender, instance, **kwargs):
    if instance.pk:
        previous_meta_hotel = Hotel.objects.get(pk=instance.pk).meta_hotel
        if previous_meta_hotel != instance.meta_hotel:
            delete_meta_hotel_if_no_hotels(previous_meta_hotel, minus_one_if_pre_save=True)
        
def delete_meta_hotel_if_no_hotels(meta_hotel, minus_one_if_pre_save = False):
    try:
        hotels = Hotel.objects.filter(meta_hotel=meta_hotel)
        hotels_amount = hotels.count()
        if minus_one_if_pre_save:
            hotels_amount -= 1
        if hotels_amount <= 0:
            meta_hotel.delete()
    except AttributeError:
        pass