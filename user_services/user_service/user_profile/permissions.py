from rest_framework import permissions


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Safe methods allowed for all.
    Updates only if auth_user_id == request.user.id
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        return str(obj.auth_user_id) == str(getattr(user, "id", None))
