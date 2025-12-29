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
        print(f"DEBUG: SendRequest: Requester={request.user.id}, Target={target_id}")

        if not target_id:
            return Response(
                {"detail": "target_user_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        from user_profile.models import Profile
        
        # 1. Get Requester Profile to check role (since token might not have it)
        try:
            requester_profile = Profile.objects.get(auth_user_id=request.user.id)
            if not requester_profile.role:
                print(f"DEBUG: Profile exists but role is empty. Defaulting to 'client'.")
                requester_profile.role = "client"
                requester_profile.save()
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
        
        # ... logic ...
        
        obj, created = ConnectionRequest.objects.get_or_create(
            requester_id=str(request.user.id),
            target_id=str(target_id)
        )
        print(f"DEBUG: ConnectionRequest created? {created}. Obj ID: {obj.id}, Status: {obj.status}")

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
        user_id = str(request.user.id)
        print(f"DEBUG: PendingRequests for target={user_id}")
        # Only show requests for the authenticated user as target
        qs = ConnectionRequest.objects.filter(target_id=user_id, status=ConnectionRequest.STATUS_PENDING)
        print(f"DEBUG: Found {qs.count()} pending requests.")
        serializer = ConnectionRequestSerializer(qs, many=True)
        return Response(serializer.data)


class ApproveRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req_id = request.data.get("request_id")
        action = request.data.get("action")
        print(f"DEBUG: ApproveRequest: ID={req_id}, Action={action}")

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
        
        print(f"DEBUG: Request {req.id} new status: {req.status}")

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


class ConnectedUsers(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id)
        print(f"DEBUG: ConnectedUsers for user={user_id}")
        
        # 1. As Target (People who requested me and I approved) -> Clients following me
        received_ids = ConnectionRequest.objects.filter(
            target_id=user_id, 
            status=ConnectionRequest.STATUS_APPROVED
        ).values_list('requester_id', flat=True)
        
        # 2. As Requester (People I requested and they approved) -> Professionals I follow
        sent_ids = ConnectionRequest.objects.filter(
            requester_id=user_id, 
            status=ConnectionRequest.STATUS_APPROVED
        ).values_list('target_id', flat=True)
        
        # Combine unique IDs
        connected_ids = set(received_ids) | set(sent_ids)
        print(f"DEBUG: Connected IDs: {connected_ids}")
        
        from user_profile.models import Profile
        from user_profile.serializers import PublicProfileSerializer
        
        profiles = Profile.objects.filter(auth_user_id__in=connected_ids)
        serializer = PublicProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data)
        

class RemoveConnection(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        target_id = request.data.get("target_user_id")
        if not target_id:
            return Response({"detail": "target_user_id required"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = str(request.user.id)
        target_id = str(target_id)
        
        print(f"DEBUG: RemoveConnection: User={user_id} removing Target={target_id}")

        # Find the connection (can be requester or target)
        connection = ConnectionRequest.objects.filter(
            (Q(requester_id=user_id) & Q(target_id=target_id)) |
            (Q(requester_id=target_id) & Q(target_id=user_id)),
            status=ConnectionRequest.STATUS_APPROVED
        ).first()

        if not connection:
            return Response({"detail": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)

        connection.delete()
        print(f"DEBUG: Connection removed between {user_id} and {target_id}")

        return Response({"detail": "Connection removed"}, status=status.HTTP_200_OK)
