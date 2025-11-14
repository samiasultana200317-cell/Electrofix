from django.urls import path
from ..views import (
    RegisterView, LoginView, UserProfileView,
    ServiceListView, ServiceDetailView, CategoryListView,
    BookingListView, BookingDetailView, CreateBookingView
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Services
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<str:_id>/', ServiceDetailView.as_view(), name='service-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Bookings
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', CreateBookingView.as_view(), name='booking-create'),
    path('bookings/<str:_id>/', BookingDetailView.as_view(), name='booking-detail'),
]