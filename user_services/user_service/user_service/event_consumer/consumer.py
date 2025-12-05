import json
import pika
import os
from django.conf import settings
from user_profile.models import Profile  # change to your model

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue="user_created", durable=True)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        print("Event received:", event)

        Profile.objects.create(
            user_id=event["id"],
            email=event["email"],
            name=event["name"]
        )

        print("User profile created successfully")

    channel.basic_consume(
        queue="user_created",
        on_message_callback=callback,
        auto_ack=True
    )

    print("User Service consumer listening for events...")
    channel.start_consuming()
