# follow/admin.py
from django.contrib import admin

from .models import ConnectionRequest


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("requester_id", "target_id", "status", "created_at", "acted_at")
    list_filter = ("status",)
    search_fields = ("requester_id", "target_id")
