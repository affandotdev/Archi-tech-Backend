from rest_framework.permissions import BasePermission


class IsArchitect(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "role")
            and request.user.is_authenticated
            and request.user.role == "architect"
        )


class IsEngineer(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "role")
            and request.user.is_authenticated
            and request.user.role == "engineer"
        )


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, "role")
            and request.user.is_authenticated
            and request.user.role == "client"
        )


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
