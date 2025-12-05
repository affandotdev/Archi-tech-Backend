from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model
from src.presentation.serializers.user_serializers import RegisterSerializer
from src.common.utils.otp_utils import create_email_otp
from src.common.utils.email_utils import send_otp_email
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from django.utils.timezone import now, timedelta


from infrastructure.message_broker import publish_user_created_event


User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        user = User.objects.create_user(
            email=data["email"],
            password=data["password"]
        )

        user.first_name = data.get("first_name", "")
        user.last_name = data.get("last_name", "")
        user.phone = data.get("phone", "")
        user.role = data.get("role", "client")
        user.is_active = False
        user.is_verified = False
        user.save()

        # 📤 PUBLISH EVENT TO RABBITMQ
        publish_user_created_event(
            user_id=user.id,
            email=user.email,
            username=user.first_name or user.email,
            first_name=user.first_name,
            role=user.role,
            last_name=user.last_name

            

        )

        # Create OTP and send email
        otp_obj = create_email_otp(user.email, purpose='registration')
        send_otp_email(user.email, otp_obj.otp, purpose='registration')

        return Response(
            {"status": "success", "message": "Registered. Verify OTP sent to email."},
            status=status.HTTP_201_CREATED
        )


class TrustDeviceView(APIView):
    def post(self, request):
        response = Response({"message": "Device trusted for 30 days"})

        expiry = now() + timedelta(days=30)

        response.set_cookie(
            "trusted_device",
            "yes",
            expires=expiry,
            httponly=True,
            samesite="Lax",
            secure=False
        )

        return response
