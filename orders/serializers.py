# orders/serializers.py
from rest_framework import serializers
from .models import Order
from accounts.serializers import CustomUserSerializer
from services.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomUserSerializer(read_only=True)
    business = CustomUserSerializer(read_only=True)
    service = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'business', 'service', 'status', 'created_at']