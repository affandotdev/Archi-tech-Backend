from django.db import models


class AdminDailyReport(models.Model):
    total_users = models.IntegerField(default=0)
    total_projects = models.IntegerField(default=0)
    total_profession_requests = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Daily Report - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
