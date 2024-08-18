from django.shortcuts import render

# Create your views here.


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.db.models import Count, F
from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from django.core.cache import cache

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "This is a protected view!"})


@api_view(['GET', 'POST'])
def hotel_list_create(request):
    if request.method == 'GET':
        queryset = Hotel.objects.all().annotate(
            available_rooms=Count('rooms', filter=F('rooms__is_available'))
        )

        # Filters
        city = request.query_params.get('city')
        star_rating = request.query_params.get('star_rating')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        available_rooms = request.query_params.get('available_rooms')

        if city:
            queryset = queryset.filter(city=city)
        if star_rating:
            queryset = queryset.filter(star_rating=star_rating)
        if min_price:
            queryset = queryset.filter(rooms__base_price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(rooms__base_price_per_night__lte=max_price)
        if available_rooms:
            queryset = queryset.filter(available_rooms__gte=1)

        serializer = HotelSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log or return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        check_in_date = serializer.validated_data['check_in_date']
        check_out_date = serializer.validated_data['check_out_date']

        # Calculate total price
        total_days = (check_out_date - check_in_date).days
        total_price = total_days * room.dynamic_price

        serializer.save(total_price=total_price)

        # Update room availability and booked dates
        room.booked_dates.append({
            'check_in': str(check_in_date),
            'check_out': str(check_out_date)
        })
        room.is_available = False
        room.save()


class RoomListCreateView(APIView):
    def get(self, request, hotel_id):
        # Retrieve available rooms for the specified hotel
        queryset = Room.objects.filter(hotel_id=hotel_id, is_available=True)

        # Apply filters
        room_type = request.query_params.get('room_type', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)

        if room_type:
            queryset = queryset.filter(room_type=room_type)
        if min_price is not None:
            queryset = queryset.filter(base_price_per_night__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(base_price_per_night__lte=max_price)

        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()  # Copy to modify
        data['hotel'] = hotel_id  # Add the hotel field automatically

        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)  # Ensure hotel is set correctly
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCancelView(APIView):
    def post(self, request, *args, **kwargs):
        booking = Booking.objects.get(pk=kwargs['pk'])

        if booking.booking_status == 'Cancelled':
            return Response({'status': 'Booking already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
 
        # Update booking status
        booking.booking_status = 'Cancelled'
        booking.save()

        # Implement refund logic here

        return Response({'status': 'Booking cancelled'}, status=status.HTTP_200_OK)


class HotelListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    def get_queryset(self):
        queryset = Hotel.objects.all().annotate(
            available_rooms=Count('rooms', filter=F('rooms__is_available'))
        )

        # Apply filters as needed

        return queryset

    def perform_create(self, serializer):
        serializer.save()

class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        hotel = Hotel.objects.get(id=self.kwargs['hotel_id'])
        serializer.save(hotel=hotel)
