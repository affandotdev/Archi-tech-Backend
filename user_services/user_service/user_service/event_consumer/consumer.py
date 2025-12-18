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

        # HANDLE USER CREATED
        if event.get("event") == "USER_CREATED":
            Profile.objects.update_or_create(
                auth_user_id=event["id"],
                defaults={
                    "first_name": event.get("first_name", ""),
                    "last_name": event.get("last_name", ""),
                    "role": event.get("role", "client")
                },
            )
            print(f"✅ USER_CREATED synced for user {event['id']}")

        # HANDLE USER UPDATED
        elif event.get("event") == "USER_UPDATED":
            Profile.objects.update_or_create(
                auth_user_id=event["id"],
                defaults={
                    "first_name": event.get("first_name", ""),
                    "last_name": event.get("last_name", ""),
                    "bio": event.get("bio", ""),
                    "location": event.get("location", ""),
                    "role": event.get("role", "client")
                },
            )
            print(f"🔄 USER_UPDATED synced for user {event['id']}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=False
    )

    print("🟢 User Service RabbitMQ Consumer Listening…")
    channel.start_consuming()
