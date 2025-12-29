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
        try:
            from django.conf import settings
            import traceback
            
            print(f"DEBUG_JWT_KEY: {settings.SIMPLE_JWT.get('SIGNING_KEY')}")
            print(f"DEBUG_AUTH_HEADER: {request.headers.get('Authorization')}")
            print(f"DEBUG_USER: {request.user}")
            print(f"DEBUG_USER_AUTHENTICATED: {request.user.is_authenticated}")
            
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
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌ ERROR in SubmitProfessionRequestView: {str(e)}")
            print(f"❌ TRACEBACK:\n{error_trace}")
            return Response(
                {"error": str(e), "trace": error_trace},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        user.role = req.requested_role  # Update role to requested role
        user.profession_verified = True
        user.save()

        # Publish RabbitMQ event to sync with user_service
        from src.infrastructure.message_broker import publish_user_role_updated_event
        publish_user_role_updated_event(user.id, user.role, is_verified=True)

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
