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
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


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
