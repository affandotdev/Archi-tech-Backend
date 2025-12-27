from rest_framework import serializers
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = "__all__"

    def get_last_message(self, obj):
        # Since conversation_id is a UUIDField and not a ForeignKey, we must filter manually
        last_msg = Message.objects.filter(conversation_id=obj.id).order_by('-created_at').first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
