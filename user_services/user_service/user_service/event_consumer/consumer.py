import json
import pika
import os
from user_profile.models import Profile

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        print("📥 Event received:", event)

        auth_id = event.get("id")
        first = event.get("first_name") or ""
        last = event.get("last_name") or ""
        role = event.get("role") or "client"

        # 🔥 FIX: ALWAYS UPDATE OR CREATE
        profile, created = Profile.objects.update_or_create(
            auth_user_id=auth_id,
            defaults={
                "first_name": first,
                "last_name": last,
                "role": role,
            },
        )

        print("✅ Profile saved:", profile.auth_user_id)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=True,
    )

    print("🟢 RabbitMQ consumer listening…")
    channel.start_consuming()





#testing