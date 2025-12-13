import json
import pika
from django.conf import settings
from users.models import User


def start_profile_consumer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    settings.RABBITMQ_USER,
                    settings.RABBITMQ_PASS
                )
            )
        )

        channel = connection.channel()
        channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

        print("📥 Auth service is listening for PROFILE_UPDATED events...")

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)

                if data.get("event") != "PROFILE_UPDATED":
                    return

                user_id = data.get("auth_user_id")
                first_name = data.get("first_name")
                last_name = data.get("last_name")
                role = data.get("role")

                User.objects.filter(id=user_id).update(
                    first_name=first_name,
                    last_name=last_name
                )

                print(f"✔ Updated auth user {user_id} from PROFILE_UPDATED event")

            except Exception as e:
                print("❌ Error handling event:", e)

        channel.basic_consume(
            queue=settings.RABBITMQ_QUEUE,
            on_message_callback=callback,
            auto_ack=True
        )

        channel.start_consuming()

    except Exception as e:
        print("❌ Consumer crashed:", e)
