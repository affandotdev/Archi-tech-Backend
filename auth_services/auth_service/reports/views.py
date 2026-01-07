from rest_framework import permissions, viewsets

from .models import AdminDailyReport
from .serializers import AdminDailyReportSerializer


class AdminDailyReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows admins to view daily reports.
    """

    queryset = AdminDailyReport.objects.all().order_by("-created_at")
    serializer_class = AdminDailyReportSerializer
    permission_classes = [permissions.IsAdminUser]
