from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import ProfessionalRequest  
from src.presentation.serializers.ProfessionRequest import ProfessionRequestSerializer


class SubmitProfessionRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.conf import settings
        print(f"DEBUG_JWT_KEY: {settings.SIMPLE_JWT.get('SIGNING_KEY')}")
        print(f"DEBUG_AUTH_HEADER: {request.headers.get('Authorization')}")
        user = request.user

        if ProfessionalRequest.objects.filter(
            user=user, status__in=["pending", "approved"]
        ).exists():
            return Response(
                {"message": "A profession request is already pending or approved"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfessionRequestSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(
                {
                    "message": "Profession request submitted successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )



class ApproveProfessionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        req = get_object_or_404(ProfessionalRequest, pk=pk)

        if req.status == "approved":
            return Response(
                {"message": "Request already approved"},
                status=status.HTTP_400_BAD_REQUEST
            )

        req.status = "approved"
        req.admin_comment = request.data.get("comment", "")
        req.reviewed_by = request.user
        req.save()

        user = req.user
        user.profession_verified = True
        user.save()

        # OPTIONAL: emit RabbitMQ event here
        # publish_event("PROFESSION_VERIFIED", user.id, user.role)

        return Response({"message": "Request approved"}, status=status.HTTP_200_OK)




class RejectProfessionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        req = get_object_or_404(ProfessionalRequest, pk=pk)

        if req.status == "rejected":
            return Response(
                {"message": "Request already rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if req.status == "approved":
            return Response(
                {"message": "Approved request cannot be rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        req.status = "rejected"
        req.admin_comment = request.data.get("comment", "")
        req.reviewed_by = request.user
        req.save()

        return Response(
            {"message": "Request rejected"},
            status=status.HTTP_200_OK
        )










class ListProfessionRequestsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = ProfessionalRequest.objects.all().order_by("-created_at")
        serializer = ProfessionRequestSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
