# src/presentation/controllers/login_controller.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
    






class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=401)

        # ALWAYS generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # If MFA is enabled → send tokens + mfa_required
        if user.has_mfa:
            return Response({
                "mfa_required": True,
                "user_id": user.id,
                "access": access_token,
                "refresh": refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
                "role": user.role,
            }, status=200)

        # If MFA not enabled → normal login
        return Response({
            "mfa_required": False,
            "access": access_token,
            "refresh": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            },
            "role": user.role,
        }, status=200)
