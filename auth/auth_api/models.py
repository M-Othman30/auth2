# auth_api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('garage_owner', 'Garage Owner'),
    )

    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='client')

    def __str__(self):
        return self.username
