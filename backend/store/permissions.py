# Permissions
from rest_framework import permissions

class HasStoreOwnerRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'store_owner'


class IsOwnerOfStore(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user