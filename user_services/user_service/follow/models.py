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

    requester = models.ForeignKey(User, related_name="sent_connection_requests", on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name="received_connection_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    acted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("requester", "target")
        indexes = [
            models.Index(fields=["target", "status"]),
            models.Index(fields=["requester", "status"]),
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
        return f"{self.requester} -> {self.target} ({self.status})"
