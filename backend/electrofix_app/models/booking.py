from djongo import models as djongo_models
from .user import User
from .service import Service
from .technician import Technician

class Booking(djongo_models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    _id = djongo_models.ObjectIdField()
    customer = djongo_models.ForeignKey(User, on_delete=djongo_models.CASCADE, related_name='bookings')
    service = djongo_models.ForeignKey(Service, on_delete=djongo_models.CASCADE)
    technician = djongo_models.ForeignKey(Technician, on_delete=djongo_models.SET_NULL, null=True, blank=True)
    booking_date = djongo_models.DateTimeField()
    address = djongo_models.TextField()
    problem_description = djongo_models.TextField()
    status = djongo_models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = djongo_models.DecimalField(max_digits=10, decimal_places=2)
    created_at = djongo_models.DateTimeField(auto_now_add=True)
    updated_at = djongo_models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self._id} - {self.customer.get_full_name()}"