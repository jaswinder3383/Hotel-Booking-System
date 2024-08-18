from django.contrib import admin

# Register your models here.
from .models import Hotel, Room, Booking

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
