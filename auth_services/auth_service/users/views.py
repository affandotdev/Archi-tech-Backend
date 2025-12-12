from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.infrastructure.message_broker import publish_profile_updated


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data

    update_fields = {}

    if "first_name" in data:
        update_fields["first_name"] = data["first_name"]

    if "last_name" in data:
        update_fields["last_name"] = data["last_name"]

    if "bio" in data:
        update_fields["bio"] = data["bio"]

    if "location" in data:
        update_fields["location"] = data["location"]

    if "phone" in data:
        update_fields["phone"] = data["phone"]

    if "role" in data:
        update_fields["role"] = data["role"]

    # 🔥 SEND CORRECT EVENT NAME
    publish_profile_updated(user.id, update_fields)

    return Response({
        "message": "Profile update event sent successfully",
        "updated_fields": update_fields
    }, status=200)
