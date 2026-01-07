# import json
# import pika
# from django.conf import settings
# from users.models import User


# def start_profile_consumer():
#     try:
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(
#                 host=settings.RABBITMQ_HOST,
#                 port=settings.RABBITMQ_PORT,
#                 credentials=pika.PlainCredentials(
#                     settings.RABBITMQ_USER,
#                     settings.RABBITMQ_PASS
#                 )
#             )
#         )

#         channel = connection.channel()
#         channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True)

#         print("📥 Auth service is listening for PROFILE_UPDATED events...")

#         def callback(ch, method, properties, body):
#             try:
#                 data = json.loads(body)

#                 if data.get("event") != "PROFILE_UPDATED":
#                     return

#                 user_id = data.get("auth_user_id")
#                 first_name = data.get("first_name")
#                 last_name = data.get("last_name")
#                 role = data.get("role")

#                 User.objects.filter(id=user_id).update(
#                     first_name=first_name,
#                     last_name=last_name
#                 )

#                 print(f"✔ Updated auth user {user_id} from PROFILE_UPDATED event")

#             except Exception as e:
#                 print("❌ Error handling event:", e)

#         channel.basic_consume(
#             queue=settings.RABBITMQ_QUEUE,
#             on_message_callback=callback,
#             auto_ack=True
#         )

#         channel.start_consuming()

#     except Exception as e:
#         print("❌ Consumer crashed:", e)


# import json
# import os
# import pika
# from django.contrib.auth import get_user_model

# User = get_user_model()

# RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
# RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
# RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
# RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


# def start_profile_consumer():
#     credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(
#             host=RABBITMQ_HOST,
#             virtual_host=RABBITMQ_VHOST,
#             credentials=credentials,
#         )
#     )

#     channel = connection.channel()
#     channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

#     def callback(ch, method, properties, body):
#         event = json.loads(body)

#         if event.get("event") != "PROFILE_UPDATED":
#             ch.basic_ack(delivery_tag=method.delivery_tag)
#             return

#         user_id = event.get("user_id")
#         changes = event.get("changes", {})

#         SAFE_FIELDS = {"first_name", "last_name"}

#         clean_data = {k: v for k, v in changes.items() if k in SAFE_FIELDS}

#         if clean_data:
#             User.objects.filter(id=user_id).update(**clean_data)
#             print(f"✔ Updated auth user {user_id} from PROFILE_UPDATED event")

#         ch.basic_ack(delivery_tag=method.delivery_tag)

#     channel.basic_consume(
#         queue=RABBITMQ_QUEUE,
#         on_message_callback=callback,
#         auto_ack=False,
#     )

#     print("🟢 Auth Service listening for PROFILE_UPDATED events")
#     channel.start_consuming()


import json
import os

import pika
from django.contrib.auth import get_user_model

User = get_user_model()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


def start_profile_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            virtual_host=RABBITMQ_VHOST,
            credentials=credentials,
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def callback(ch, method, properties, body):
        event = json.loads(body)

        if event.get("event") != "PROFILE_UPDATED":
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        user_id = event.get("user_id")
        changes = event.get("changes", {})

        ALLOWED_FIELDS = {"first_name", "last_name"}

        clean_changes = {k: v for k, v in changes.items() if k in ALLOWED_FIELDS}

        if clean_changes:
            User.objects.filter(id=user_id).update(**clean_changes)
            print(f"✅ Auth user {user_id} updated: {clean_changes}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=False,
    )

    print("🟢 Auth Service listening for PROFILE_UPDATED events")
    channel.start_consuming()
