from django.urls import path

from .views import (ProjectCreateAPIView, ProjectDetailAPIView,
                    ProjectImageUploadAPIView, ProjectStatsAPIView,
                    PublicProjectListAPIView)

urlpatterns = [
    path("projects/", ProjectCreateAPIView.as_view()),
    path("projects/<int:project_id>/images/", ProjectImageUploadAPIView.as_view()),
    path("projects/<int:project_id>/", ProjectDetailAPIView.as_view()),
    path("users/<str:user_id>/projects/", PublicProjectListAPIView.as_view()),
    path("internal/stats/projects/", ProjectStatsAPIView.as_view()),
]
