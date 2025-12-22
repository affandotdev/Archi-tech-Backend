from django.apps import AppConfig
import threading
import os


class UserServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_service"

    # def ready(self):
    #     if os.environ.get("RUN_MAIN") != "true":
    #         return
    #     from user_service.event_consumer.consumer import start

    #     threading.Thread(
    #         target=start,
    #         daemon=True
    #     ).start()
