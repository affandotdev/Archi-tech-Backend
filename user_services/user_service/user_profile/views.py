import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Profile
from .serializers import ProfileSerializer
from infrastructure.message_broker import publish_profile_updated

logger = logging.getLogger(__name__)


def process_full_name(data):
    """Convert full_name into first_name + last_name."""
    if "full_name" in data:
        full_name = data.pop("full_name")
        if full_name:
            parts = full_name.strip().split(None, 1)
            data["first_name"] = parts[0] if len(parts) else ""
            data["last_name"] = parts[1] if len(parts) > 1 else ""
    return data


class ProfileMeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # Accept JSON (from SPA), form-data, and multipart (for future extensibility)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_user_id(self, request):
        return str(getattr(request.user, "id", None))

    def get(self, request):
        user_id = request.user.id

        profile, created = Profile.objects.get_or_create(auth_user_id=user_id)

        # Calculate Connection Count
        from django.db.models import Q
        from follow.models import ConnectionRequest
        
        connection_count = ConnectionRequest.objects.filter(
            (Q(requester_id=str(user_id)) | Q(target_id=str(user_id))),
            status=ConnectionRequest.STATUS_APPROVED
        ).count()

        serializer = ProfileSerializer(profile)
        data = serializer.data
        data['connection_count'] = connection_count

        return Response({
            "message": "Profile fetched successfully",
            "data": data
        })

    def post(self, request):
        user_id = self.get_user_id(request)
        if not user_id:
            return Response({"detail": "Unauthenticated"}, status=401)

        existing = Profile.objects.filter(auth_user_id=user_id).first()
        if existing:
            return Response(ProfileSerializer(existing, context={"request": request}).data, status=200)

        data = request.data.copy()
        data["auth_user_id"] = user_id
        data = process_full_name(data)

        serializer = ProfileSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer.save()

        publish_profile_updated(user_id, serializer.data)

        return Response(serializer.data, status=201)

    def put(self, request):
        user_id = self.get_user_id(request)
        if not user_id:
            return Response({"detail": "Unauthenticated"}, status=401)

        profile = Profile.objects.filter(auth_user_id=user_id).first()

        data = request.data.copy()
        data["auth_user_id"] = user_id
        data = process_full_name(data)

        serializer = ProfileSerializer(
            profile, data=data, context={"request": request}
        ) if profile else ProfileSerializer(data=data, context={"request": request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer.save()

       
        publish_profile_updated(user_id, serializer.data)
        

        return Response(serializer.data, status=200 if profile else 201)

    def patch(self, request):
        user_id = self.get_user_id(request)
        if not user_id:
            return Response({"detail": "Unauthenticated"}, status=401)

        profile = Profile.objects.filter(auth_user_id=user_id).first()
        if not profile:
            return Response({"error": "Profile not found"}, status=404)

        data = process_full_name(request.data.copy())
        serializer = ProfileSerializer(
            profile, data=data, partial=True, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer.save()
  














       
        publish_profile_updated(user_id, serializer.data)

        return Response(serializer.data, status=200)


class ProfileImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """Upload profile image (avatar)"""
        user_id = str(getattr(request.user, "id", None))
        if not user_id:
            return Response({"detail": "Unauthenticated"}, status=401)

        profile = Profile.objects.filter(auth_user_id=user_id).first()

        if not profile:
            # Create profile if it doesn't exist
            profile = Profile.objects.create(auth_user_id=user_id)

        if "profile_image" in request.FILES:
            profile.avatar = request.FILES["profile_image"]
            profile.save()
            serializer = ProfileSerializer(profile, context={"request": request})
            return Response(serializer.data, status=200)
        else:
            return Response({"error": "No image file provided"}, status=400)


class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self, id):
        return Profile.objects.filter(id=id).first()

    def get(self, request, id):
        profile = self.get_object(id)
        if not profile:
            return Response({"detail": "Profile not found"}, status=404)

        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data, status=200)

    def patch(self, request, id):
        profile = self.get_object(id)
        if not profile:
            return Response({"detail": "Profile not found"}, status=404)

        data = process_full_name(request.data.copy())
        serializer = ProfileSerializer(profile, data=data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer.save()

        # 🔥 Publish Event
        publish_profile_updated(profile.auth_user_id, serializer.data)

        return Response(serializer.data, status=200)

    def delete(self, request, id):
        profile = self.get_object(id)
        if not profile:
            return Response({"detail": "Profile not found"}, status=404)

        profile.delete()
        profile.delete()
        return Response({"detail": "Profile deleted"}, status=204)