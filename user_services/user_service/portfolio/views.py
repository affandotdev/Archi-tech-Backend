from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Project, ProjectImage
from .serializers import ProjectSerializer



from rest_framework.parsers import MultiPartParser, FormParser

class ProjectCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            project = serializer.save(owner_id=request.user.id)
            return Response(
                ProjectSerializer(project, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProjectImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(
                id=project_id,
                owner_id=request.user.id
            )
        except Project.DoesNotExist:
            return Response(
                {"detail": "Project not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        images = request.FILES.getlist("images")

        if not images:
            return Response(
                {"detail": "No images provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for img in images:
            ProjectImage.objects.create(
                project=project,
                image=img
            )

        return Response(
            {"message": "Images uploaded successfully"},
            status=status.HTTP_201_CREATED
        )






class PublicProjectListAPIView(APIView):
    def get(self, request, user_id):
        # Allow admins to see everything, otherwise filter by public visibility
        if getattr(request.user, 'role', None) == 'admin':
             projects = Project.objects.filter(owner_id=user_id).order_by("-created_at")
        else:
            projects = Project.objects.filter(
                owner_id=user_id,
                visibility="public"
            ).order_by("-created_at")

        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, project_id, user):
        try:
            return Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

    def get(self, request, project_id):
        project = self.get_object(project_id, request.user)
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # private project check
        if project.visibility == "private":
            is_owner = (request.user.is_authenticated and project.owner_id == request.user.id)
            is_admin = getattr(request.user, 'role', None) == 'admin'
            
            if not (is_owner or is_admin):
                return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        project = self.get_object(project_id, request.user)
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check ownership
        if str(project.owner_id) != str(request.user.id) and getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to edit this project."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectSerializer(project, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = self.get_object(project_id, request.user)
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check ownership
        if str(project.owner_id) != str(request.user.id) and getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "You do not have permission to delete this project."}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


