from rest_framework import serializers

from .models import Project, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["id", "image", "order"]


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        extra_kwargs = {"owner_id": {"read_only": True}}
        fields = [
            "id",
            "owner_id",
            "title",
            "project_type",
            "location",
            "year",
            "description",
            "visibility",
            "has_3d",
            "model_file",
            "images",
            "created_at",
        ]

    def create(self, validated_data):
        if validated_data.get("model_file"):
            validated_data["has_3d"] = True
        return super().create(validated_data)
