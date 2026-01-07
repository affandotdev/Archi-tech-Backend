from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "is_active",
            "is_verified",
            "has_mfa",
            "date_joined",
            "last_login",
            "phone",
            "first_name",
            "last_name",
            "profile_image",
        ]

    def get_profile_image(self, obj):
        try:
            if hasattr(obj, "userprofile") and obj.userprofile.profile_image:
                request = self.context.get("request")
                if request:
                    return request.build_absolute_uri(obj.userprofile.profile_image.url)
                return obj.userprofile.profile_image.url
        except Exception:
            pass
        return None
