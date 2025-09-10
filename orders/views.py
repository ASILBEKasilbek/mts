# orders/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsCustomer, IsBusiness
from django.conf import settings
import hashlib
import requests

class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)
        # Signal orqali notification

    @swagger_auto_schema(operation_description="Buyurtma berish.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class OrderStatus(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsBusiness]
        return [IsAuthenticated]

class ProcessPayment(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="To'lovni qayta ishlash (Click).")
    def post(self, request):
        order_id = request.data['order_id']
        amount = request.data['amount']
        merchant_trans_id = f'order_{order_id}'
        sign_string = f"{settings.CLICK_MERCHANT_ID}{settings.CLICK_SERVICE_ID}{settings.CLICK_SECRET_KEY}{merchant_trans_id}{amount}"
        sign = hashlib.md5(sign_string.encode()).hexdigest()
        payload = {
            'service_id': settings.CLICK_SERVICE_ID,
            'merchant_id': settings.CLICK_MERCHANT_ID,
            'amount': amount,
            'transaction_param': merchant_trans_id,
            'sign_string': sign,
        }
        response = requests.post('https://my.click.uz/services/pay', json=payload)
        if response.status_code == 200:
            order = Order.objects.get(id=order_id)
            order.status = 'paid'
            order.save()
            return Response({'status': 'success', 'data': response.json()})
        return Response({'status': 'error'}, status=400)