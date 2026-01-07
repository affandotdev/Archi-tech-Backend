from rest_framework import serializers

from .models import AdminDailyReport


class AdminDailyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDailyReport
        fields = "__all__"
