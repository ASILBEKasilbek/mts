# admin_panel/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from accounts.permissions import IsAdmin  # Import tuzatildi
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from services.models import BaseService
from django.core.mail import send_mail

class AdminUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(operation_description="Admin uchun foydalanuvchilarni ko'rish.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ApproveService(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(operation_description="Xizmatni tasdiqlash.")
    def patch(self, request, id):
        service = BaseService.objects.get(id=id)
        service.status = 'confirmed'
        service.save()
        send_mail('Tasdiqlandi', 'Sizning xizmatingiz tasdiqlandi.', 'admin@uzmat.uz', [service.author.email])
        return Response({'status': 'approved'})