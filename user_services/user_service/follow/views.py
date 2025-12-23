# follow/views.py
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ConnectionRequest
from .serializers import ConnectionRequestSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class SendConnectionRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        target_id = request.data.get("target_user_id")

        if not target_id:
            return Response(
                {"detail": "target_user_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        from user_profile.models import Profile
        
        # 1. Get Requester Profile to check role (since token might not have it)
        try:
            requester_profile = Profile.objects.get(auth_user_id=request.user.id)
            requester_role = requester_profile.role.lower()
        except Profile.DoesNotExist:
            # Self-healing: Create missing profile if not found
            print(f"DEBUG: Profile missing for user {request.user.id}. Creating default Client profile.")
            requester_profile = Profile.objects.create(
                auth_user_id=request.user.id,
                role="client",
                first_name="Client", # Placeholder
                last_name="User"
            )
            requester_role = "client"

        print(f"DEBUG: User {request.user.id} has profile role='{requester_role}'")
        
        if requester_role != "client":
            return Response(
                {"detail": f"only clients can send requests (your role: {requester_role})"},
                status=status.HTTP_403_FORBIDDEN
            )

        if str(request.user.id) == str(target_id):
            return Response(
                {"detail": "cannot request yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        from user_profile.models import Profile
        target_profile = get_object_or_404(Profile, auth_user_id=target_id)

        if target_profile.role not in ["architect", "engineer"]:
            return Response(
                {"detail": "target must be architect or engineer"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # We need a User instance for the ForeignKey. 
        # If using ServiceUser, we might need a local User stub or change model to use integer ID.
        # Assuming ConnectionRequest models.ForeignKey(User) expects a real DB row.
        # If User table is not synced, we have a problem.
        # BUT, typically we sync User table via RabbitMQ too? 
        # If not, ConnectionRequest should use auth_user_id (Integer) instead of ForeignKey.
        
        # For now, let's assume User table exists and is synced or we get the user.
        # We don't need User model lookup anymore. We trust the Profile check we did earlier.
        
        obj, created = ConnectionRequest.objects.get_or_create(
            requester_id=str(request.user.id),
            target_id=str(target_id)
        )

        if not created:
            return Response(
                {"detail": "request already exists", "status": obj.status},
                status=status.HTTP_200_OK
            )

        serializer = ConnectionRequestSerializer(
            obj, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PendingRequests(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Only show requests for the authenticated user as target
        qs = ConnectionRequest.objects.filter(target_id=str(request.user.id), status=ConnectionRequest.STATUS_PENDING)
        serializer = ConnectionRequestSerializer(qs, many=True)
        return Response(serializer.data)


class ApproveRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req_id = request.data.get("request_id")
        action = request.data.get("action")

        if not req_id or action not in ["approve", "reject"]:
            return Response(
                {"detail": "request_id and valid action required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        req = get_object_or_404(ConnectionRequest, pk=req_id)

        if str(req.target_id) != str(request.user.id):
            return Response(
                {"detail": "not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        if req.status != ConnectionRequest.STATUS_PENDING:
            return Response(
                {"detail": "request already handled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == "approve":
            req.approve()
        else:
            req.reject()

        return Response(
            {"detail": "ok", "status": req.status},
            status=status.HTTP_200_OK
        )



class CheckAccess(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, target_id):
        if not request.user or not request.user.is_authenticated:
            return Response({"allowed": False})

        allowed = ConnectionRequest.objects.filter(
            status=ConnectionRequest.STATUS_APPROVED
        ).filter(
            Q(requester_id=str(request.user.id), target_id=str(target_id)) |
            Q(requester_id=str(target_id), target_id=str(request.user.id))
        ).exists()

        return Response({"allowed": allowed})
