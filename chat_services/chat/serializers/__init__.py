from rest_framework import serializers

from ..models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    unread_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = "__all__"

    def get_last_message(self, obj):
        last_msg = (
            Message.objects.filter(conversation_id=obj.id)
            .order_by("-created_at")
            .first()
        )
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        user_id = self.context.get("user_id")
        if not user_id:
            # Fallback if context not passed, try request query params
            request = self.context.get("request")
            if request:
                user_id = request.query_params.get("user_id")

        if user_id:
            from ..models import Notification

            return Notification.objects.filter(
                user_id=user_id,
                type="NEW_MESSAGE",
                reference_id=str(obj.id),
                is_read=False,
            ).count()
        return 0


from .notification import NotificationSerializer
