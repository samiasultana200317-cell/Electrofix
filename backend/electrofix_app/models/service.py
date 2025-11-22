from djongo import models

class Service(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    category = models.CharField(
        max_length=50, 
        choices=[
            ('repair', 'Repair'),
            ('maintenance', 'Maintenance'),
            ('installation', 'Installation'),
            ('inspection', 'Inspection')
        ]
    )
    image = models.URLField(blank=True, null=True)
    features = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': str(self._id),
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'duration': self.duration,
            'category': self.category,
            'image': self.image,
            'features': self.features,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }