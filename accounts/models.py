# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from services.models import Product  # Favorites uchun

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    name = models.CharField(max_length=255, blank=True)
    avatar = models.URLField(blank=True, null=True)
    is_company = models.BooleanField(default=False)
    favorites = models.ManyToManyField(Product, related_name='favorited_by', blank=True)

    def __str__(self):
        return self.name or self.username