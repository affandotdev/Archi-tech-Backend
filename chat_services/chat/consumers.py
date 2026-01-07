import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .fcm_service import send_push_notification
from .models import Message, Notification
from .redis_presence import is_user_online, user_offline, user_online


@sync_to_async
def create_message(conversation_id, sender_id, content):
    from django.utils import timezone

    from .models import Conversation

    msg = Message.objects.create(
        conversation_id=conversation_id, sender_id=sender_id, content=content
    )

    Conversation.objects.filter(id=conversation_id).update(updated_at=timezone.now())

    # Fetch conversation to get participants
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        # Notify other participants
        if isinstance(conversation.participants, list):
            for participant_id in conversation.participants:
                # Ensure we don't notify the sender
                if str(participant_id) != str(sender_id):
                    # 1. Create DB Notification for Navbar
                    try:
                        Notification.objects.create(
                            user_id=str(participant_id),
                            type="NEW_MESSAGE",
                            reference_id=conversation_id,
                            is_read=False,
                        )
                    except Exception as ex:
                        print(f"Failed to create notification record: {ex}")

                    # 2. Send FCM Notification for Popup/Push
                    try:
                        send_push_notification(
                            user_id=str(participant_id),
                            title="New Message",
                            body=f"New message from {sender_id}: {content[:30]}...",
                        )
                    except Exception as e:
                        print(
                            f"Failed to send push notification to {participant_id}: {e}"
                        )
    except Exception as e:
        print(f"Error notifying participants: {e}")

    return msg


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print(f"Connecting... Route params: {self.scope['url_route']['kwargs']}")
        try:
            self.conversation_id = str(
                self.scope["url_route"]["kwargs"]["conversation_id"]
            )
            self.room_group_name = f"chat_{self.conversation_id}"
            print(f"Room group name: {self.room_group_name}")

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()
            print("Connection accepted!")
        except Exception as e:
            print(f"Error in connect: {e}")
            raise e

    async def disconnect(self, close_code):
        print(f"Disconnecting... Code: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return

        msg_type = data.get("type", "chat_message")
        sender_id = data.get("sender_id") or data.get("from")

        if not sender_id:
            await self.send(
                text_data=json.dumps({"error": "sender_id (or 'from') is required"})
            )
            return

        if msg_type in [
            "call.start",
            "call.accept",
            "call.reject",
            "call.end",
            "webrtc.offer",
            "webrtc.answer",
            "webrtc.ice",
        ]:

            target_user = data.get("to")
            payload = data.get("payload", {})

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "signaling_message",
                    "msg_type": msg_type,
                    "sender_id": sender_id,
                    "to": target_user,
                    "payload": payload,
                },
            )
            return

        message_content = data.get("message")

        if not message_content:

            await self.send(
                text_data=json.dumps({"error": "message content required for chat"})
            )
            return

        msg = await create_message(self.conversation_id, sender_id, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender_id": sender_id,
                "content": msg.content,
                "created_at": str(msg.created_at),
            },
        )

    async def signaling_message(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": event["msg_type"],
                    "from": event["sender_id"],
                    "to": event.get("to"),
                    "payload": event.get("payload"),
                }
            )
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


def handle_notifications(sender_id, receiver_id, conversation_id):
    if is_user_online(receiver_id):
        return

    Notification.objects.create(
        user_id=receiver_id,
        type="NEW_MESSAGE",
        reference_id=conversation_id,
    )

    send_push_notification(
        user_id=receiver_id,
        title="New message",
        body="You have a new message",
    )
