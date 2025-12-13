from rest_framework import serializers
from users.models import ProfessionalRequest

class ProfessionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalRequest
        fields = "__all__"
        read_only_fields = ["status", "admin_comment", "requested_at", "updated_at"]
