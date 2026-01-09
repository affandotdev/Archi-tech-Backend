from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from src.presentation.serializers.profile_serializer import \
    UserProfileSerializer
from users.models import UserProfile
from src.common.utils.cloudinary_uploader import upload_to_cloudinary

class UserProfileController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id  # Extracted from JWT token decoded by UserService

        profile, created = UserProfile.objects.get_or_create(user_id=user_id)
        serializer = UserProfileSerializer(profile)

        return Response(
            {"message": "Profile fetched successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class UserProfileUpdateController(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_id = request.user.id

        profile, created = UserProfile.objects.get_or_create(user_id=user_id)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Profile updated successfully", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class UserProfileImageUploadController(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user_id = request.user.id
        profile, created = UserProfile.objects.get_or_create(user_id=user_id)

        image = request.FILES.get("profile_image")

        if not image:
            return Response(
                {"error": "No image uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔹 CLOUDINARY UPLOAD (THIS IS THE NEW PART)
        upload_result = upload_to_cloudinary(
            image,
            folder=f"profile_images/{user_id}"
        )

        profile.profile_image_url = upload_result["url"]
        profile.profile_image_public_id = upload_result["public_id"]
        profile.save()

        return Response(
            {
                "message": "Image uploaded successfully",
                "image_url": profile.profile_image_url
            },
            status=status.HTTP_200_OK
        )