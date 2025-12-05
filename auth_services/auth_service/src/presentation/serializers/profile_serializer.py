from rest_framework import serializers
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "full_name",
            "bio",
            "profile_image",
            "phone",
            "location",
            "skills",
            "experience",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        # user field is ignored automatically
        validated_data.pop("user", None)
        return super().update(instance, validated_data)
