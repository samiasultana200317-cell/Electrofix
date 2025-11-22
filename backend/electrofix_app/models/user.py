from djongo import models
import bcrypt
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class User(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.JSONField(default=dict)
    role = models.CharField(
        max_length=20, 
        choices=[
            ('customer', 'Customer'),
            ('admin', 'Admin'),
            ('technician', 'Technician')
        ], 
        default='customer'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_token(self):
        payload = {
            'user_id': str(self._id),
            'email': self.email,
            'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def to_dict(self):
        return {
            'id': str(self._id),
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }