from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="userprofile",
        primary_key=True
    )
    user_image = models.ImageField(upload_to="user_images", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
"""

class Custom_User( AbstractUser ):
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="user_images", blank=True, default="user_images/default.jpg")

    def __str__(self):
        return f"{self.username}'s Profile"