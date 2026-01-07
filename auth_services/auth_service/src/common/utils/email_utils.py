from django.conf import settings
from django.core.mail import send_mail


def send_otp_email(email, otp, purpose="registration"):
    subject = f"{settings.DEFAULT_FROM_EMAIL} - {purpose} OTP"
    message = f"Your OTP for {purpose} is: {otp}\nIt expires in 5 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
    except Exception as e:
        # for debugging + fallback printing
        print("Error sending email:", e)
        print("OTP for", email, ":", otp)
        raise
