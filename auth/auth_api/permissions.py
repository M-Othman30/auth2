# auth_api/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'admin'

class IsGarageOwnerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'garage_owner'

class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'client'
