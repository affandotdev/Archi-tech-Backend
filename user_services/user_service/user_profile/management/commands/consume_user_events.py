import json
import time
import os
import pika
from django.core.management.base import BaseCommand
from user_profile.models import Profile

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


class Command(BaseCommand):
    help = "Consume user events from RabbitMQ"

    def handle(self, *args, **options):
        while True:
            try:
                self.stdout.write("🟡 Connecting to RabbitMQ...")

                creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOST,
                        credentials=creds,
                        heartbeat=600,
                    )
                )

                channel = connection.channel()
                channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

                self.stdout.write("🟢 User Service consuming user_events")

                def callback(ch, method, properties, body):
                    event = json.loads(body)
                    event_type = event.get("event")
                    user_id = event.get("user_id")

                    if event_type == "USER_ROLE_UPDATED":
                        Profile.objects.update_or_create(
                            auth_user_id=user_id,
                            defaults={"role": event["role"]},
                        )
                        self.stdout.write(f"✅ Role updated for user {user_id}")

                    ch.basic_ack(delivery_tag=method.delivery_tag)

                channel.basic_consume(
                    queue=RABBITMQ_QUEUE,
                    on_message_callback=callback,
                )

                channel.start_consuming()

            except Exception as e:
                self.stderr.write(f"🔴 Consumer crashed, retrying in 5s: {e}")
                time.sleep(5)
