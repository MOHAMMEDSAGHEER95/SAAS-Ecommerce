from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsPremiumTenant(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.tenant.has_active_plan():
            raise PermissionDenied("You do not have permission to access this endpoint.")
        if request.tenant.is_premium_plan():
            return True
        else:
            raise PermissionDenied("You do not have permission to access this endpoint.")