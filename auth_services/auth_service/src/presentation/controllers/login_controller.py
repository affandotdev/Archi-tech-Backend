# # src/presentation/controllers/login_controller.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from users.models import User


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(username=username, password=password)
#         if not user:
#             return Response({"detail": "Invalid credentials"}, status=401)

#         # ALWAYS generate tokens
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         # If MFA is enabled → send tokens + mfa_required
#         if user.has_mfa:
#             return Response({
#                 "mfa_required": True,
#                 "user_id": user.id,
#                 "access": access_token,
#                 "refresh": refresh_token,
#                 "user": {
#                     "id": user.id,
#                     "email": user.email,
#                     "role": user.role,
#                 },
#                 "role": user.role,
#             }, status=200)

#         # If MFA not enabled → normal login
#         return Response({
#             "mfa_required": False,
#             "access": access_token,
#             "refresh": refresh_token,
#             "user": {
#                 "id": user.id,
#                 "email": user.email,
#                 "role": user.role,
#             },
#             "role": user.role,
#         }, status=200)


# src/presentation/controllers/login_controller.py

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, UserProfile


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Check if user exists first
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            # Avoid explicit "user not found" for security if desired, but for debugging/UX:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # 2. Check if user is active (verified)
        if not user_obj.is_active:
            return Response(
                {"detail": "Account is not verified. Please verify your email."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 3. Authenticate (check password)
        # We explicitly pass username=email because ModelBackend expects 'username' arg
        user = authenticate(request=request, username=email, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        try:
            profile = UserProfile.objects.get(user=user)
            full_name = profile.full_name
            # Ensure we get a valid URL if image exists
            if profile.profile_image:
                try:
                    avatar_url = request.build_absolute_uri(profile.profile_image.url)
                except:
                    avatar_url = profile.profile_image.url
            else:
                avatar_url = None
        except UserProfile.DoesNotExist:
            avatar_url = None
            full_name = ""

        response_data = {
            "mfa_required": user.has_mfa,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": full_name,
                "avatar_url": avatar_url,
            },
            "role": user.role,
        }

        if user.has_mfa:
            response_data["user_id"] = user.id

        return Response(response_data, status=status.HTTP_200_OK)
