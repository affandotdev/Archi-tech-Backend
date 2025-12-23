from django.urls import path
from .views import (
    ProjectCreateAPIView,
    ProjectImageUploadAPIView,
    PublicProjectListAPIView,
    ProjectDetailAPIView,
)

urlpatterns = [
    path("projects/", ProjectCreateAPIView.as_view()),
    path("projects/<int:project_id>/images/", ProjectImageUploadAPIView.as_view()),
    path("projects/<int:project_id>/", ProjectDetailAPIView.as_view()),
    path("users/<str:user_id>/projects/", PublicProjectListAPIView.as_view()),
]
