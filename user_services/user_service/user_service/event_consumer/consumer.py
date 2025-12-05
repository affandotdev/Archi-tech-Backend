import json
import pika
import os
from django.conf import settings
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
        print("🔥 EVENT RECEIVED:", event)

        auth_user_id = event.get("id")
        first_name = event.get("first_name", "")
        last_name = event.get("last_name", "")
        role = event.get("role", "")

        # Create or update Profile
        profile, created = Profile.objects.update_or_create(
            auth_user_id=event["id"],
            defaults={
            "first_name": event.get("first_name", ""),
            "last_name": event.get("last_name", ""),
            "role": event.get("role", "client"),   # default client
        }
    )


        print("✅ Profile saved for user:", auth_user_id)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=True
    )

    print("👂 User Service listening for events...")
    channel.start_consuming()
