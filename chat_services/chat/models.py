import uuid
from django.db import models


class Conversation(models.Model):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.JSONField(
        help_text="List of user UUIDs participating in the conversation"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.UUIDField()
    sender_id = models.CharField(max_length=255, help_text="User ID from auth_service")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message {self.id} in {self.conversation.id}"


class FCMToken(models.Model):
    user_id = models.CharField(max_length=255)
    token = models.CharField(max_length=512)
    device_type = models.CharField(max_length=50, default='web')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'token')

class Notification(models.Model):
    user_id = models.CharField(max_length=255)
    type = models.CharField(max_length=50) # NEW_MESSAGE, etc.
    reference_id = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Token for {self.user_id}"
