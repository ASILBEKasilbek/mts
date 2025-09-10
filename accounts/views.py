# accounts/views.py
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusiness
from rest_framework import serializers
from rest_framework.response import Response



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Yangi foydalanuvchini ro'yxatdan o'tkazish.",
        request_body=RegisterSerializer,
        responses={201: CustomUserSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LoginView(TokenObtainPairView):
    @swagger_auto_schema(operation_description="Tizimga kirish va JWT token olish.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class CompanyList(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_company=True)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class CompanyDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_company=True)
    serializer_class = CustomUserSerializer
    lookup_field = 'slug'  # CustomUser ga slug qo'shing agar kerak bo'lsa
    permission_classes = [IsAuthenticated]

class MyProductStats(generics.RetrieveAPIView):
    serializer_class = serializers.DictField()  # Statistics uchun
    permission_classes = [IsBusiness]

    def get(self, request, id):
        from services.models import Product
        product = Product.objects.get(id=id, author=request.user)
        return Response(product.statistics)

class MyApplicationStats(generics.RetrieveAPIView):
    serializer_class = serializers.DictField()
    permission_classes = [IsBusiness]

    def get(self, request, id):
        # Placeholder
        return Response({'views': 100, 'clicks': 50})