from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from users.models import User

User = get_user_model()


class CustomModelBackend(ModelBackend):
    """
    Custom authentication backend that authenticates users by email instead of username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user by email and password.
        """
        if username is None:
            username = kwargs.get("email")

        if username is None or password is None:
            return None

        try:
            # Look for user by email instead of username
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None


# users/backends.py


# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return None

#         if user.check_password(password) and user.is_active:
#             return user
#         return None
