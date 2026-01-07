from rest_framework import serializers
from users.models import ProfessionalRequest


class ProfessionRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = ProfessionalRequest
        fields = "__all__"
        read_only_fields = [
            "user",
            "status",
            "admin_comment",
            "created_at",
            "updated_at",
            "user_email",
            "reviewed_by",
        ]
