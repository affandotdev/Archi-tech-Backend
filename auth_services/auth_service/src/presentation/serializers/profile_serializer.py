from rest_framework import serializers
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "full_name",
            "bio",
            "profile_image",
            "phone",
            "role",
            "location",
            "skills",
            "experience",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "role"]

    def update(self, instance, validated_data):
        # user field is ignored automatically
        validated_data.pop("user", None)
        return super().update(instance, validated_data)
