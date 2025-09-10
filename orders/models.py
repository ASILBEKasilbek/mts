# orders/models.py
from django.db import models
from accounts.models import CustomUser
from services.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('paid', 'Paid'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    business = models.ForeignKey(CustomUser, related_name='received_orders', on_delete=models.CASCADE)
    service = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.service.title}"