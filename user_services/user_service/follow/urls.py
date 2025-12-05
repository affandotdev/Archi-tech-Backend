# follow/urls.py
from django.urls import path
from .views import SendConnectionRequest, PendingRequests, ApproveRequest, CheckAccess

urlpatterns = [
    path("send/", SendConnectionRequest.as_view(), name="follow-send"),
    path("pending/", PendingRequests.as_view(), name="follow-pending"),
    path("approve/", ApproveRequest.as_view(), name="follow-approve"),
    path("check/<int:target_id>/", CheckAccess.as_view(), name="follow-check"),
]
