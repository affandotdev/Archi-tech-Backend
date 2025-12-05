import json
import pika
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "user_events")


def publish_user_created_event(user_id, email, username):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )

        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        message = {
            "event": "USER_CREATED",
            "id": user_id,
            "email": email,
            "username": username
        }

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(message)
        )

        print("📤 Sent USER_CREATED event:", message)
        connection.close()

    except Exception as e:
        print("❌ RabbitMQ publish failed:", str(e))
