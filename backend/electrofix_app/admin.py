from django.contrib import admin
from .models.user import User
from .models.service import Service
from .models.booking import Booking
from .models.technician import Technician

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'role', 'created_at']
    search_fields = ['email', 'name']
    list_filter = ['role', 'created_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_active']
    search_fields = ['name', 'category']
    list_filter = ['category', 'is_active']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    def mongo_id(self, obj):
        return str(obj._id)
    mongo_id.short_description = 'ID'

    list_display = ['mongo_id', 'user', 'service', 'status', 'scheduled_date']
    search_fields = ['user__email', 'service__name']
    list_filter = ['status', 'scheduled_date']

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience', 'rating']
    search_fields = ['user__email', 'specialization']
    list_filter = ['experience', 'rating']