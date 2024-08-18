from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    star_rating = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField()
    amenities = models.JSONField()

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    )

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    base_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    dynamic_price_modifier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    is_available = models.BooleanField(default=True)
    booked_dates = models.JSONField(default=list)

    def __str__(self):
        return f'{self.hotel.name} - Room {self.room_number}'

    @property
    def dynamic_price(self):
        return self.base_price_per_night * self.dynamic_price_modifier

class Booking(models.Model):
    BOOKING_STATUS = (
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='Booked')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')

    def __str__(self):
        return f'Booking {self.id} - {self.room.hotel.name} - Room {self.room.room_number}'
