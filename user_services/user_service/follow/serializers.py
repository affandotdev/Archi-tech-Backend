# follow/serializers.py
from rest_framework import serializers
from .models import ConnectionRequest
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ConnectionRequestSerializer(serializers.ModelSerializer):
    requester = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    target = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ConnectionRequest
        fields = ("id", "requester", "target", "status", "created_at", "acted_at")
        read_only_fields = ("status", "created_at", "acted_at")

    def create(self, validated_data):
        # Ensure requester is the request user
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["requester"] = request.user
        return super().create(validated_data)
