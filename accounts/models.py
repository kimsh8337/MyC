from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='followings'
            )
    admin = models.BooleanField(default=False)
    level = models.IntegerField(default=1)
    
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        )
    nickname = models.CharField(max_length=100, default='Iron man')
    message = models.CharField(max_length=500, default='Hello!')
