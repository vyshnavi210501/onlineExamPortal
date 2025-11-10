from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(blank=True, null=True)
    profile_picture=models.ImageField(upload_to='profiles/', blank=True, null=True)
    contact_number=models.CharField(max_length=11)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


    