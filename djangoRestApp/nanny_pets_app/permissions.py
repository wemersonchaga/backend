from rest_framework import permissions

class IsTutorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'tutor')

class IsCuidadorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'cuidador')
