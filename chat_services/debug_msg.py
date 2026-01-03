
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_services.settings')
django.setup()

from chat.models import Conversation, Message
from chat.serializers import ConversationSerializer

print("--- DEBUG START ---")
convs = Conversation.objects.all()
print(f"Total Conversations: {convs.count()}")

for c in convs:
    print(f"\nConversation {c.id}:")
    msgs = Message.objects.filter(conversation_id=c.id)
    count = msgs.count()
    print(f"  Message Count: {count}")
    
    if count > 0:
        last = msgs.order_by('-created_at').first()
        print(f"  Last Message Object: {last}")
        print(f"  Last Message ID: {last.id}")
        
        # Test Serializer logic directly
        serializer = ConversationSerializer(c, context={'user_id': '4'}) # Mock user_id
        data = serializer.data
        print(f"  Serializer Last Message: {data.get('last_message')}")
    else:
        print("  No messages.")
        
print("--- DEBUG END ---")
