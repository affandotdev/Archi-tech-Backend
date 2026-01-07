import os

import django
from django.conf import settings
from django.urls import resolve, reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.main.settings")
django.setup()

try:
    path = "/api/auth/admin/users/"
    match = resolve(path)
    print(f"SUCCESS: Resolves to {match.func.__name__} in {match.func.__module__}")
except Exception as e:
    print(f"FAILURE: Could not resolve {path}: {e}")

try:
    path = "/api/auth/admin/dashboard/stats/"
    match = resolve(path)
    print(f"SUCCESS: Resolves to {match.func.__name__} in {match.func.__module__}")
except Exception as e:
    print(f"FAILURE: Could not resolve {path}: {e}")
