from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication



class ConversationCreateView(APIView):
    def post(self, request):
        print(f"ConversationCreateView POST hit with data: {request.data}")
        participants = request.data.get("participants", [])
        if not participants or len(participants) < 2:
            return Response({"error": "At least 2 participants required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Sort to ensure consistent ordering for comparison
        participants.sort()
        
        # Check if conversation exists (Naive implementation for JSONField)
        # In production, use a ManyToMany User relation for efficient querying
        existing_convs = Conversation.objects.filter(is_active=True)
        for conv in existing_convs:
            if sorted(conv.participants) == participants:
                return Response(ConversationSerializer(conv).data, status=status.HTTP_200_OK)

        # Create new
        serializer = ConversationSerializer(data={"participants": participants})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationListView(APIView):
    def get(self, request):
        user_id = getattr(request, 'user_id', None)
        # Fallback if user_id is not set by middleware but we assume it might be passed as query param for dev, 
        # or we just return empty if not auth.
        # Actually, let's look at how MessageCreateView does it. It uses request.user_id.
        
        if not user_id:
             # Try to get from query param strictly for testing if needed, or return 400
             user_id = request.query_params.get("user_id")
        
        if not user_id:
            return Response({"error": "User ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # DEBUG PRINTS
            print(f"ConversationListView: Fetching for user_id: {user_id} (Type: {type(user_id)})")
            
            # Fetch all and filter in python to be safe against SQLite/JSON type mismatches (str vs int)
            # and SQLite contains lookup issues.
            all_conversations = Conversation.objects.all().order_by('-updated_at')
            
            filtered_conversations = []
            target_uid_str = str(user_id)
            
            for conv in all_conversations:
                # participants should be a list, but check just in case
                if isinstance(conv.participants, list):
                    # Check if user_id matches any participant (casting to string for comparison)
                    if any(str(p) == target_uid_str for p in conv.participants):
                        filtered_conversations.append(conv)
                        
            print(f"ConversationListView: Found {len(filtered_conversations)} convs (Python Filter)")

            serializer = ConversationSerializer(filtered_conversations, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageCreateView(APIView):
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListView(APIView):
    def get(self, request, conversation_id):
        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)





class MessageCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["sender_id"] = request.user_id  # force from token

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
