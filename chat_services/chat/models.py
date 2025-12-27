import uuid
from django.db import models


class Conversation(models.Model):
    """
    Represents a chat between two or more users.
    Users are referenced by their UUIDs from auth_service.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.JSONField(
        help_text="List of user UUIDs participating in the conversation"
    )
    # Example: ["uuid-user-1", "uuid-user-2"]

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message in a conversation.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation_id = models.UUIDField()
    sender_id = models.CharField(max_length=255, help_text="User ID from auth_service")

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message {self.id} in {self.conversation.id}"
