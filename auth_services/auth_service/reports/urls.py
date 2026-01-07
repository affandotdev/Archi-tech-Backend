from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminDailyReportViewSet

router = DefaultRouter()
router.register(r"daily-reports", AdminDailyReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
