from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Use related_name for easier access
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default_avatar.png')

    def __str__(self):
        return f'{self.user.username} Profile'
