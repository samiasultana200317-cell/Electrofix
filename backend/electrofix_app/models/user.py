from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from djongo import models as djongo_models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('technician', 'Technician'),
        ('admin', 'Admin'),
    )
    
    _id = djongo_models.ObjectIdField()
    email = djongo_models.EmailField(unique=True)
    first_name = djongo_models.CharField(max_length=30)
    last_name = djongo_models.CharField(max_length=30)
    phone = djongo_models.CharField(max_length=15, blank=True)
    address = djongo_models.TextField(blank=True)
    user_type = djongo_models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    
    is_active = djongo_models.BooleanField(default=True)
    is_staff = djongo_models.BooleanField(default=False)
    is_superuser = djongo_models.BooleanField(default=False)
    
    date_joined = djongo_models.DateTimeField(auto_now_add=True)
    last_login = djongo_models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"