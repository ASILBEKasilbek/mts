# accounts/permissions.py
from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'business'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

# View'larda ishlatish uchun or operatorini to'g'ri qilish: [permissions.IsAuthenticated, IsBusiness] yoki custom
class IsBusinessOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role in ['business', 'admin'])