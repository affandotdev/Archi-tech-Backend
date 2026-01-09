from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.main"

    def ready(self):
        import src.common.utils.cloudinary_config