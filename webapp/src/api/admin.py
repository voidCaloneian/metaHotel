from django.contrib import admin
from .models import MetaHotel, Hotel, HotelHistory

admin.site.register(MetaHotel)
admin.site.register(Hotel)
admin.site.register(HotelHistory)
