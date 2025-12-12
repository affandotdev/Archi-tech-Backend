from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.main"

    def ready(self):
        # Start RabbitMQ Consumer
        try:
            from src.infrastructure.profile_consumer import run
            run()
            print("🟢 AUTH SERVICE CONSUMER STARTED")
        except Exception as e:
            print("❌ Failed to start consumer:", e)
