from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from functools import partial
from django.utils import timezone


class MetaHotel(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.id

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, blank=True, max_length=100, related_name='hotels')

    def __str__(self):
        return self.name
    

class HotelHistory(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, related_name='history')
    meta_hotel = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, related_name='history')
    linked_datetime = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'Hotel: {self.hotel} linked to {self.meta_hotel}'

@receiver(pre_save, sender=Hotel)
def create_hotel_history(sender, instance, **kwargs):
    def create_hotel_history_object(instance):
        HotelHistory.objects.create(
            hotel = instance,
            meta_hotel = instance.supplier
        )
    try:
        previous_supplier = Hotel.objects.get(id=instance.id)
        if previous_supplier != instance.supplier:
            transaction.on_commit(partial(
                create_hotel_history_object, instance=instance
            ))
    except Hotel.DoesNotExist:
        transaction.on_commit(partial(
            create_hotel_history_object, instance=instance
        ))
            
    