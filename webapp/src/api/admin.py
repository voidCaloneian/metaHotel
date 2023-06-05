from django.contrib import admin
from .models import MetaHotel, Hotel, HotelHistory


admin.site.register(MetaHotel)
admin.site.register(Hotel)

class HotelHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('linked_datetime',)

admin.site.register(HotelHistory, HotelHistoryAdmin)

