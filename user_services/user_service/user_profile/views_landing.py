from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Profile
from .serializers import PublicProfileSerializer

class LandingProfessionals(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        architects = Profile.objects.filter(role="architect")
        engineers = Profile.objects.filter(role="engineer")

        return Response({
            "architects": PublicProfileSerializer(
                architects, many=True, context={"request": request}
            ).data,
            "engineers": PublicProfileSerializer(
                engineers, many=True, context={"request": request}
            ).data
        })
