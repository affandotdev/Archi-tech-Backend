# follow/urls.py
from django.urls import path
from .views import SendConnectionRequest, PendingRequests, ApproveRequest, CheckAccess, ConnectedUsers

urlpatterns = [
    path("send/", SendConnectionRequest.as_view(), name="follow-send"),
    path("pending/", PendingRequests.as_view(), name="follow-pending"),
    path("approve/", ApproveRequest.as_view(), name="follow-approve"),
    path("check/<str:target_id>/", CheckAccess.as_view(), name="follow-check"),
    path("connections/", ConnectedUsers.as_view(), name="follow-connections"),
]
