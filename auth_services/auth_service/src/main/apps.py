from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.main"

    def ready(self):
        from src.infrastructure.profile_consumer import start_profile_consumer
        import threading

        # Start consumer in background thread
        threading.Thread(target=start_profile_consumer, daemon=True).start()
