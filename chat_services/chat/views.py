from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import JWTAuthentication
from .models import Conversation, FCMToken, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationCreateView(APIView):
    def post(self, request):
        print(f"ConversationCreateView POST hit with data: {request.data}")
        participants = request.data.get("participants", [])
        if not participants or len(participants) < 2:
            return Response(
                {"error": "At least 2 participants required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants.sort()

        existing_convs = Conversation.objects.filter(is_active=True)
        for conv in existing_convs:
            if sorted(conv.participants) == participants:
                return Response(
                    ConversationSerializer(conv).data, status=status.HTTP_200_OK
                )

        serializer = ConversationSerializer(data={"participants": participants})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationListView(APIView):
    def get(self, request):
        user_id = getattr(request, "user_id", None)
        if not user_id:
            user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:

            print(
                f"ConversationListView: Fetching for user_id: {user_id} (Type: {type(user_id)})"
            )

            all_conversations = Conversation.objects.all().order_by("-updated_at")

            filtered_conversations = []
            target_uid_str = str(user_id)

            for conv in all_conversations:
                if isinstance(conv.participants, list):

                    if any(str(p) == target_uid_str for p in conv.participants):
                        filtered_conversations.append(conv)

            print(
                f"ConversationListView: Found {len(filtered_conversations)} convs (Python Filter)"
            )

            serializer = ConversationSerializer(
                filtered_conversations,
                many=True,
                context={"user_id": user_id, "request": request},
            )
            return Response(serializer.data)
        except Exception as e:
            import traceback

            traceback.print_exc()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        data["sender_id"] = request.user_id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterFCMTokenView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        token = request.data.get("token")

        if not user_id or not token:
            return Response(
                {"error": "user_id and token are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        FCMToken.objects.update_or_create(
            user_id=user_id, token=token, defaults={"device_type": "web"}
        )

        return Response({"status": "Token registered successfully"})


from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id") or getattr(
            request, "user_id", None
        )
        if not user_id:
            return Response(
                {"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST
            )

        notifs = Notification.objects.filter(user_id=user_id, is_read=False)
        serializer = NotificationSerializer(notifs, many=True)
        return Response(serializer.data)


class NotificationMarkReadView(APIView):
    def post(self, request, notification_id=None):
        # 1. Bulk Mark by Conversation ID
        conversation_id = request.data.get("conversation_id")
        user_id = request.data.get("user_id")

        if conversation_id and user_id:
            updated_count = Notification.objects.filter(
                user_id=user_id, reference_id=str(conversation_id), is_read=False
            ).update(is_read=True)
            return Response({"status": "marked read", "count": updated_count})

        # 2. Single Notification Mark (Legacy / Specific)
        if notification_id:
            try:
                notif = Notification.objects.get(id=notification_id)
                notif.is_read = True
                notif.save()
                return Response({"status": "marked read"})
            except Notification.DoesNotExist:
                return Response(
                    {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"error": "Invalid request parameters"}, status=status.HTTP_400_BAD_REQUEST
        )
