from djongo import models as djongo_models

class Category(djongo_models.Model):
    _id = djongo_models.ObjectIdField()
    name = djongo_models.CharField(max_length=100)
    description = djongo_models.TextField(blank=True)
    icon = djongo_models.CharField(max_length=50, blank=True)
    is_active = djongo_models.BooleanField(default=True)
    
    class Meta:
        db_table = 'categories'
    
    def __str__(self):
        return self.name

class Service(djongo_models.Model):
    SERVICE_STATUS = (
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    )
    
    _id = djongo_models.ObjectIdField()
    name = djongo_models.CharField(max_length=200)
    description = djongo_models.TextField()
    price = djongo_models.DecimalField(max_digits=10, decimal_places=2)
    duration = djongo_models.IntegerField(help_text="Duration in minutes")
    category = djongo_models.ForeignKey(Category, on_delete=djongo_models.CASCADE)
    image = djongo_models.URLField(blank=True)
    status = djongo_models.CharField(max_length=20, choices=SERVICE_STATUS, default='available')
    features = djongo_models.JSONField(default=list)
    created_at = djongo_models.DateTimeField(auto_now_add=True)
    updated_at = djongo_models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'services'
    
    def __str__(self):
        return self.name