# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
import bcrypt


class CustomUserSerializer(serializers.ModelSerializer):
    favorites = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'avatar', 'favorites', 'is_company', 'username', 'email', 'role']

    def get_favorites(self, obj):
        from services.serializers import ProductSerializer   # ⬅️ local import
        return ProductSerializer(obj.favorites.all(), many=True).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        user = CustomUser(**validated_data)
        user.password = hashed_password
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'name', 'role', 'avatar', 'is_company']
