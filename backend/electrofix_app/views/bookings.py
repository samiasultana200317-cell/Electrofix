from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Booking
from ..serializers import BookingSerializer, BookingCreateSerializer
from ..utils.auth import get_user_from_request

class BookingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        user = get_user_from_request(self.request)
        return Booking.objects.filter(customer=user)

class BookingDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    lookup_field = '_id'

class CreateBookingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingCreateSerializer
    
    def perform_create(self, serializer):
        user = get_user_from_request(self.request)
        service = serializer.validated_data['service']
        booking = serializer.save(
            customer=user,
            total_price=service.price,
            status='pending'
        )
        return booking