from django.db import models





class MetaHotel(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, blank=True, max_length=100, related_name='hotels')

class HotelHistory(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, related_name='history')
    meta_hotel = models.ForeignKey(MetaHotel, on_delete=models.SET_NULL, null=True, related_name='history')


