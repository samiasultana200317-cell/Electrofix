from rest_framework import serializers
from ..models.booking import Booking
from .user import UserSerializer
from .service import ServiceSerializer

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    service_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'service', 'service_id', 'appliance_type', 'brand', 'model',
            'problem_description', 'address', 'scheduled_date', 'time_slot',
            'status', 'total_cost'
        ]
        read_only_fields = ['id', 'user', 'total_cost', 'status']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance._id)
        return data