from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from src.presentation.serializers.auth_schemas import ChangePasswordSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        user = request.user
        old = request.data.get('old_password')
        new = request.data.get('new_password')
        if not user.check_password(old):
            return Response({"status":"error","message":"Old password incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new)
        user.save()
        return Response({"status":"success","message":"Password changed"}, status=status.HTTP_200_OK)
