# follow/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # string 'users.User' or your configured user


class ConnectionRequest(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    )

    # Decoupling from local User table to support Microservices/UUIDs
    requester_id = models.CharField(max_length=100, db_index=True)
    target_id = models.CharField(max_length=100, db_index=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    acted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("requester_id", "target_id")
        indexes = [
            models.Index(fields=["target_id", "status"]),
            # models.Index(fields=["requester_id", "status"]), # Already covered by unique_together prefix or db_index
        ]

    def approve(self):
        self.status = self.STATUS_APPROVED
        self.acted_at = timezone.now()
        self.save()

    def reject(self):
        self.status = self.STATUS_REJECTED
        self.acted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.requester_id} -> {self.target_id} ({self.status})"
