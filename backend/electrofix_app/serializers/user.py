from rest_framework import serializers
from ..models.user import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'phone', 'address', 'role']
        read_only_fields = ['id', 'role']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance._id)
        return data