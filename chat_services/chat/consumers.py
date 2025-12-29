# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Message, Conversation
# from asgiref.sync import sync_to_async




# @sync_to_async
# def create_message(conversation_id, sender_id, content):
#     return Message.objects.create(
#         conversation_id=conversation_id,
#         sender_id=sender_id,
#         content=content
#     )



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.conversation_id = str(self.scope["url_route"]["kwargs"]["conversation_id"])
#         self.room_group_name = f"chat_{self.conversation_id}"

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get("message")
#         sender_id = data.get("sender_id")

#         # Save message to DB (sync → async bridge)
#         msg = Message.objects.create(
#             conversation_id=self.conversation_id,
#             sender_id=sender_id,
#             content=message
#         )

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 "message": msg.content,
#                 "sender_id": sender_id,
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps(event))





import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message

@sync_to_async
def create_message(conversation_id, sender_id, content):
    from django.utils import timezone
    from .models import Conversation
    
    msg = Message.objects.create(
        conversation_id=conversation_id,
        sender_id=sender_id,
        content=content
    )

    Conversation.objects.filter(id=conversation_id).update(updated_at=timezone.now())
    
    return msg

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print(f"Connecting... Route params: {self.scope['url_route']['kwargs']}")
        try:
            self.conversation_id = str(self.scope["url_route"]["kwargs"]["conversation_id"])
            self.room_group_name = f"chat_{self.conversation_id}"
            print(f"Room group name: {self.room_group_name}")

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            print("Connection accepted!")
        except Exception as e:
            print(f"Error in connect: {e}")
            raise e

    async def disconnect(self, close_code):
        print(f"Disconnecting... Code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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
             await self.send(text_data=json.dumps({"error": "sender_id (or 'from') is required"}))
             return

        if msg_type in [
            "call.start", "call.accept", "call.reject", "call.end",
            "webrtc.offer", "webrtc.answer", "webrtc.ice"
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
                    "payload": payload
                }
            )
            return


        message_content = data.get("message")
        
        if not message_content:

             await self.send(text_data=json.dumps({"error": "message content required for chat"}))
             return

        msg = await create_message(
            self.conversation_id,
            sender_id,
            message_content
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender_id": sender_id,
                "content": msg.content,
                "created_at": str(msg.created_at)
            }
        )

    async def signaling_message(self, event):
     
        await self.send(text_data=json.dumps({
            "type": event["msg_type"],
            "from": event["sender_id"],
            "to": event.get("to"),
            "payload": event.get("payload")
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
