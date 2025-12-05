from django.urls import path
from .views import ProfileMeAPIView, ProfileDetailAPIView, ProfileImageUploadAPIView


urlpatterns = [
    path("me/", ProfileMeAPIView.as_view(), name="profile-me"),
    path("upload-image/", ProfileImageUploadAPIView.as_view(), name="profile-upload-image"),
    path("<uuid:id>/", ProfileDetailAPIView.as_view(), name="profile-detail"),
]
