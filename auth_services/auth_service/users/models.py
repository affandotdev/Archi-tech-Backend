from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('architect', 'Architect'),
        ('engineer', 'Engineer'),
        ('client', 'Client'),
        ('admin', 'Admin'),
    )

    username = None  # ❗ Remove username field (optional but recommended)
    email = models.EmailField(unique=True)  # ❗ Make email required & unique

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    has_mfa = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"        # 🔥 IMPORTANT
    REQUIRED_FIELDS = []            # 🔥 IMPORTANT

    def __str__(self):
        return self.email


class EmailOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=30, default='registration')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        indexes = [
            models.Index(fields=['email', 'purpose', 'created_at']),
        ]


class MFADevice(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='mfa_device')
    secret = models.CharField(max_length=64, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    skills = models.JSONField(default=list, blank=True)
    experience = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
