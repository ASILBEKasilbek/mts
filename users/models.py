from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None   # username ishlatmaymiz
    full_name = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=True, null=True)
    push_notifications = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "full_name"]

    def __str__(self):
        return self.email
