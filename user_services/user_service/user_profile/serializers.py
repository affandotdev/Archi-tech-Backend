from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "auth_user_id",
            "created_at",
            "updated_at",
            "full_name",
            "avatar_url",
        ]

    def get_avatar_url(self, obj):
        """
        Return absolute URL for avatar (for frontend display)
        """
        request = self.context.get("request")
        if obj.avatar:
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def get_full_name(self, obj):
        """
        Combine first_name + last_name → "John Doe"
        """
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return None





class PublicProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

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
            "avatar_url",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_avatar_url(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None