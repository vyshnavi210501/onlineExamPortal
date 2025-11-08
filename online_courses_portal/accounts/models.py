from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    role_choices = (
        ('admin','Admin'),
        ('student', 'Student'), 
        ('instructor', 'Instructor'),
    )   
    role = models.CharField(max_length=20, choices=role_choices)
    email = models.EmailField(unique=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.username
