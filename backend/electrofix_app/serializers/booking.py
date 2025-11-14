from rest_framework import serializers
from ..models import Booking

class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    technician_name = serializers.CharField(source='technician.user.get_full_name', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('service', 'booking_date', 'address', 'problem_description')