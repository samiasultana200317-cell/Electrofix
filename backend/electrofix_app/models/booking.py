from djongo import models

class Booking(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='bookings')
    appliance_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    problem_description = models.TextField()
    address = models.JSONField()
    scheduled_date = models.DateTimeField()
    time_slot = models.CharField(
        max_length=50, 
        choices=[
            ('9:00 AM - 11:00 AM', '9:00 AM - 11:00 AM'),
            ('11:00 AM - 1:00 PM', '11:00 AM - 1:00 PM'),
            ('1:00 PM - 3:00 PM', '1:00 PM - 3:00 PM'),
            ('3:00 PM - 5:00 PM', '3:00 PM - 5:00 PM')
        ]
    )
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('in-progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ], 
        default='pending'
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self._id} - {self.user.email}"

    def to_dict(self):
        return {
            'id': str(self._id),
            'user': self.user.to_dict() if self.user else None,
            'service': self.service.to_dict() if self.service else None,
            'appliance_type': self.appliance_type,
            'brand': self.brand,
            'model': self.model,
            'problem_description': self.problem_description,
            'address': self.address,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'time_slot': self.time_slot,
            'status': self.status,
            'total_cost': float(self.total_cost) if self.total_cost else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }