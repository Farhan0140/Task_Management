from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_Profile(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="userprofile",
    )
    user_image = models.ImageField(upload_to="user_images", blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
