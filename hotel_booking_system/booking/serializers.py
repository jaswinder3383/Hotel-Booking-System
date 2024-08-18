from rest_framework import serializers
from .models import Hotel, Room, Booking

class HotelSerializer(serializers.ModelSerializer):
    # available_rooms = serializers.IntegerField()
    available_rooms = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hotel
        # fields = '__all__'

        fields = ['id', 'name', 'city', 'address', 'star_rating', 'description', 'amenities', 'available_rooms']
        # fields = ['name', 'city', 'address', 'star_rating', 'description', 'amenities']

class RoomSerializer(serializers.ModelSerializer):
    dynamic_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # dynamic_price = serializers.ReadOnlyField()  # Add dynamic_price as a read-only field

    class Meta:
        
        model = Room
        # fields = '__all__'
        
        # fields = ['id', 'hotel', 'room_number', 'room_type', 'base_price_per_night', 'dynamic_price', 'is_available', 'booked_dates']
        fields = ['id', 'room_number', 'room_type', 'base_price_per_night', 'dynamic_price_modifier', 'is_available', 'booked_dates','dynamic_price']
        # read_only_fields = ['dynamic_price']  # Dynamic price is calculated and not directly set by the user

    # def create(self, validated_data):
    #     # Dynamic price is calculated and not directly set
    #     return Room.objects.create(**validated_data)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

        # fields = ['id', 'user', 'room', 'check_in_date', 'check_out_date', 'total_price', 'booking_status', 'payment_status']
