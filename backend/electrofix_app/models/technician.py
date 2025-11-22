from djongo import models

class Technician(models.Model):
    _id = models.ObjectIdField()
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='technician_profile')
    specialization = models.JSONField(default=list)  # List of specialties
    experience = models.IntegerField(default=0)  # Years of experience
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    completed_jobs = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'technicians'

    def __str__(self):
        return f"Technician: {self.user.name}"

    def to_dict(self):
        return {
            'id': str(self._id),
            'user': self.user.to_dict() if self.user else None,
            'specialization': self.specialization,
            'experience': self.experience,
            'rating': float(self.rating) if self.rating else 0.0,
            'completed_jobs': self.completed_jobs,
            'availability': self.availability,
            'current_location': self.current_location,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }