from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

def ready(self):
    from django.conf import settings
    if settings.RUN_MAIN:
        from infrastructure.message_broker import start_user_created_consumer
        start_user_created_consumer()

