# follow/views.py
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ConnectionRequest
from .serializers import ConnectionRequestSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class SendConnectionRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        target_id = request.data.get("target_user_id")
        if not target_id:
            return Response({"detail": "target_user_id required"}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.id) == str(target_id):
            return Response({"detail": "cannot request yourself"}, status=status.HTTP_400_BAD_REQUEST)

        target = get_object_or_404(User, pk=target_id)
 
        obj, created = ConnectionRequest.objects.get_or_create(requester=request.user, target=target)
        if not created:
            return Response({"detail": "request already exists", "status": obj.status}, status=status.HTTP_200_OK)

        serializer = ConnectionRequestSerializer(obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PendingRequests(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Only show requests for the authenticated user as target
        qs = ConnectionRequest.objects.filter(target=request.user, status=ConnectionRequest.STATUS_PENDING).select_related("requester")
        serializer = ConnectionRequestSerializer(qs, many=True)
        return Response(serializer.data)


class ApproveRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req_id = request.data.get("request_id")
        if not req_id:
            return Response({"detail": "request_id required"}, status=status.HTTP_400_BAD_REQUEST)
        req = get_object_or_404(ConnectionRequest, pk=req_id)
        if req.target != request.user:
            return Response({"detail": "not authorized"}, status=status.HTTP_403_FORBIDDEN)
        action = request.data.get("action", "approve")
        if action == "approve":
            req.approve()
        else:
            req.reject()
        return Response({"detail": "ok", "status": req.status})


class CheckAccess(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, target_id):
        # If user is not logged in -> False
        if not request.user or not request.user.is_authenticated:
            return Response({"allowed": False})
        # Check if there's an approved connection
        exists = ConnectionRequest.objects.filter(requester=request.user, target__id=target_id, status=ConnectionRequest.STATUS_APPROVED).exists()
        return Response({"allowed": exists})
