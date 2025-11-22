from django.urls import path
from ..views.users import update_profile, get_users

urlpatterns = [
    path('profile/', update_profile, name='update_profile'),
    path('', get_users, name='get_users'),
]