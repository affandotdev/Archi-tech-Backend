import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.main.settings")

app = Celery("auth_service")


app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["src.application.tasks"])


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
