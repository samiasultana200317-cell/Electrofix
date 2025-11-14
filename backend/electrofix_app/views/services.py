from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import Service, Category
from ..serializers import ServiceSerializer, CategorySerializer

class ServiceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer
    queryset = Service.objects.filter(status='available')

class ServiceDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    lookup_field = '_id'

class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)