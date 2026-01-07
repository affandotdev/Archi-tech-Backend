import random
from datetime import timedelta

from django.utils import timezone
from users.models import EmailOTP


class OTPService:

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_registration_otp(email):
        otp = OTPService.generate_otp()
        expires = timezone.now() + timedelta(minutes=5)

        EmailOTP.objects.create(
            email=email, otp=otp, purpose="registration", expires_at=expires
        )

        print("OTP:", otp)  # Replace with email sending later

    @staticmethod
    def verify_registration_otp(email, otp):
        try:
            obj = EmailOTP.objects.filter(email=email, purpose="registration").latest(
                "created_at"
            )
        except EmailOTP.DoesNotExist:
            return False

        if obj.is_expired():
            return False

        return obj.otp == otp
