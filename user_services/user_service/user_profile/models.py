import uuid
from django.db import models


def avatar_upload_path(instance, filename):
    return f"avatars/{instance.auth_user_id}/{filename}"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Only store the user ID from auth-service (Changed to CharField to support UUIDs)
    auth_user_id = models.CharField(max_length=100, unique=True)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)

    role = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of User {self.auth_user_id}"

