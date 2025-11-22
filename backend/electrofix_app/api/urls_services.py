from django.urls import path
from ..views.services import get_services, get_service, create_service

urlpatterns = [
    path('', get_services, name='get_services'),
    path('<str:service_id>/', get_service, name='get_service'),
    path('create/', create_service, name='create_service'),
]