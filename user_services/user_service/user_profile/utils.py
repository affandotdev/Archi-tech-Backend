import requests
from django.conf import settings

AUTH_ME_URL = "http://auth_service:8000/api/auth/me/"

def get_auth_user_from_token(token):
    """
    Validate JWT token with auth_service and return user.
    """
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(AUTH_ME_URL, headers=headers)
    except Exception:
        return None

    if response.status_code != 200:
        return None

    return response.json()
