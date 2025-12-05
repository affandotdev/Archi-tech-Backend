# follow/admin.py
from django.contrib import admin
from .models import ConnectionRequest

@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "target", "status", "created_at", "acted_at")
    list_filter = ("status",)
    search_fields = ("requester__email", "target__email")
