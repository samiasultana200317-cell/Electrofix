from rest_framework import serializers
from ..models.service import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'category', 'image', 'features', 'is_active']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance._id)
        data['price'] = float(instance.price)
        return data