import firebase_admin
from firebase_admin import credentials, messaging
from .models import FCMToken
from django.conf import settings
import os

# Initialize Firebase Admin
# We use a try-except block to avoid multiple initialization errors during reloads
try:
    if not firebase_admin._apps:
        # Check if credentials file exists
        cred_path = os.path.join(settings.BASE_DIR, 'firebase_credentials.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("[FCM] Firebase Admin Initialized successfully.")
        else:
            print(f"[FCM] WARNING: Credentials file not found at {cred_path}. Notifications will be skipped.")
except Exception as e:
    print(f"[FCM] Initialization Error: {e}")


def send_push_notification(user_id: str, title: str, body: str):
    """
    Send FCM notification to all devices registered for this user.
    """
    if not firebase_admin._apps:
        print("[FCM] Skipping: Firebase App not initialized.")
        return

    # Get all tokens for this user
    tokens_query = FCMToken.objects.filter(user_id=user_id).values_list('token', flat=True)
    tokens = list(tokens_query)

    if not tokens:
        print(f"[FCM] No tokens found for user {user_id}")
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
    )

    try:
        response = messaging.send_each_for_multicast(message)
        print(f"[FCM] Sent to {user_id}: {response.success_count} success, {response.failure_count} failed")
        
        # Optional: Cleanup invalid tokens if needed (check response.responses)
    except Exception as e:
        print(f"[FCM] Send Error: {e}")
