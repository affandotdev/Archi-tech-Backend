# follow/serializers.py
from rest_framework import serializers
from .models import ConnectionRequest
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ConnectionRequestSerializer(serializers.ModelSerializer):
    # requester = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    # target = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    requester_name = serializers.SerializerMethodField()
    requester_avatar = serializers.SerializerMethodField()
    requester_role = serializers.SerializerMethodField()  # Added role

    class Meta:
        model = ConnectionRequest
        fields = ("id", "requester_id", "requester_name", "requester_avatar", "requester_role", "target_id", "status", "created_at", "acted_at")
        read_only_fields = ("status", "created_at", "acted_at")

    def get_requester_name(self, obj):
        from user_profile.models import Profile
        try:
            profile = Profile.objects.get(auth_user_id=obj.requester_id)
            return f"{profile.first_name} {profile.last_name}".strip()
        except Profile.DoesNotExist:
            return "Unknown User"

    def get_requester_role(self, obj):
         # Try to get from Profile first, else user object
        from user_profile.models import Profile
        try:
            profile = Profile.objects.get(auth_user_id=obj.requester_id)
            return profile.role
        except Profile.DoesNotExist:
            return "unknown"

    def get_requester_avatar(self, obj):
        from user_profile.models import Profile
        try:
            profile = Profile.objects.get(auth_user_id=obj.requester_id)
            if profile.avatar:
                return f"{settings.MEDIA_URL}{profile.avatar}"
            return None
        except Profile.DoesNotExist:
            return None

    # def create(self, validated_data):
    #     # Ensure requester is the request user
    #     request = self.context.get("request")
    #     if request and request.user and request.user.is_authenticated:
    #         validated_data["requester"] = request.user
    #     return super().create(validated_data)
