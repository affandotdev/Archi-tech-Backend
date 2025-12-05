from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

    def ready(self):
        from infrastructure.message_broker import start_user_created_consumer
        start_user_created_consumer()
