from django.urls import path
from ..views.bookings import create_booking, get_user_bookings, get_booking

urlpatterns = [
    path('', create_booking, name='create_booking'),
    path('user/', get_user_bookings, name='get_user_bookings'),
    path('<str:booking_id>/', get_booking, name='get_booking'),
]