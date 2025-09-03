from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_email_confirmed= models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, related_name='confirmation', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    