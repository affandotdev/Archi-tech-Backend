import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


# ---------------------------------------------------------
# CUSTOM USER MODEL
# ---------------------------------------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ("architect", "Architect"),
        ("engineer", "Engineer"),
        ("client", "Client"),
        ("admin", "Admin"),
    )

    username = None
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    has_mfa = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# ---------------------------------------------------------
# EMAIL OTP MODEL
# ---------------------------------------------------------
class EmailOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=30, default="registration")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        indexes = [
            models.Index(fields=["email", "purpose", "created_at"]),
        ]


# ---------------------------------------------------------
# MFA DEVICE MODEL
# ---------------------------------------------------------
class MFADevice(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="mfa_device"
    )
    secret = models.CharField(max_length=64, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# ---------------------------------------------------------
# USER PROFILE MODEL (NEW)
# ---------------------------------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=50, blank=True, default="client")
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    skills = models.JSONField(default=list, blank=True)
    experience = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True, null=True)
    profile_image_public_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email


class ProfessionalRequest(models.Model):
    ROLE_CHOICES = [
        ("engineer", "Engineer"),
        ("architect", "Architect"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_requests",
    )
    requested_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    document = models.FileField(upload_to="verification_docs/", null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} requested {self.requested_role} ({self.status})"
