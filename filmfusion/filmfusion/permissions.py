from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow only authenticated admin, staff, or superuser users
        return request.user and request.user.is_authenticated and request.user.is_staff
