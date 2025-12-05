from django.urls import path
from .views import ProfileMeAPIView, ProfileDetailAPIView, ProfileImageUploadAPIView
from .views_landing import LandingProfessionals

urlpatterns = [

    # Landing page data (PUBLIC)
    path("landing/", LandingProfessionals.as_view(), name="landing"),

    path("me/", ProfileMeAPIView.as_view(), name="profile-me"),
    path("upload-image/", ProfileImageUploadAPIView.as_view(), name="profile-upload-image"),
    path("<uuid:id>/", ProfileDetailAPIView.as_view(), name="profile-detail"),

]
