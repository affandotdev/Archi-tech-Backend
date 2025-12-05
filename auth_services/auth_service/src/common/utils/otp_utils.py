import random
from datetime import timedelta
from django.utils import timezone
from users.models import EmailOTP

OTP_LENGTH = 6
OTP_TTL_MINUTES = 10

def generate_otp():
    return ''.join(str(random.randint(0,9)) for _ in range(OTP_LENGTH))

def create_email_otp(email, purpose='registration'):
    otp = generate_otp()
    expires = timezone.now() + timedelta(minutes=OTP_TTL_MINUTES)
    obj = EmailOTP.objects.create(email=email, otp=otp, purpose=purpose, expires_at=expires)
    return obj
