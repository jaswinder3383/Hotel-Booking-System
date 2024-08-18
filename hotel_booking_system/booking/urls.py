from django.urls import path
from .views import RoomListCreateView, hotel_list_create, BookingCreateView, BookingCancelView, RoomCreateView


urlpatterns = [
    path('hotels/', hotel_list_create, name='hotel-list-create'),
    path('hotels/<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('hotels/rooms/', RoomCreateView.as_view(), name='create-room-list'),
    path('bookings/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]
