from djongo import models as djongo_models
from .user import User

class Technician(djongo_models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    )
    
    _id = djongo_models.ObjectIdField()
    user = djongo_models.OneToOneField(User, on_delete=djongo_models.CASCADE)
    specialization = djongo_models.CharField(max_length=200)
    experience_years = djongo_models.IntegerField(default=0)
    hourly_rate = djongo_models.DecimalField(max_digits=8, decimal_places=2)
    rating = djongo_models.FloatField(default=0.0)
    total_reviews = djongo_models.IntegerField(default=0)
    status = djongo_models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_verified = djongo_models.BooleanField(default=False)
    skills = djongo_models.JSONField(default=list)
    available_from = djongo_models.TimeField(null=True, blank=True)
    available_to = djongo_models.TimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'technicians'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"