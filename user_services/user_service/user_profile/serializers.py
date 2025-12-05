from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "auth_user_id",
            "first_name",
            "last_name",
            "full_name",
            "bio",
            "location",
            "avatar",
            "avatar_url",
            "profile_image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "auth_user_id", "created_at", "updated_at", "full_name", "profile_image"]

    def get_avatar_url(self, obj):
        """Return absolute avatar URL so frontend shows the image properly."""
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url
        return None

    def get_full_name(self, obj):
        """Combine first_name and last_name for frontend compatibility."""
        parts = [obj.first_name, obj.last_name]
        return " ".join(filter(None, parts)) or None

    def get_profile_image(self, obj):
        """Alias for avatar_url for frontend compatibility."""
        return self.get_avatar_url(obj)
