from django.urls import path
from ..views import (
    RegisterView, LoginView, UserProfileView,
    ServiceListView, ServiceDetailView, CategoryListView,
    BookingListView, BookingDetailView, CreateBookingView,
    ProductListView, ProductDetailView, ProductCategoryListView
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    
    # Repair Services
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<str:_id>/', ServiceDetailView.as_view(), name='service-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Bookings
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', CreateBookingView.as_view(), name='booking-create'),
    path('bookings/<str:_id>/', BookingDetailView.as_view(), name='booking-detail'),
    
    # Marketplace
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<str:_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-categories/', ProductCategoryListView.as_view(), name='product-category-list'),
]