# # import json
# # import pika
# # import os
# # from user_profile.models import Profile

# # RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# # RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")

# # def start_consumer():
# #     connection = pika.BlockingConnection(
# #         pika.ConnectionParameters(host=RABBITMQ_HOST)
# #     )
# #     channel = connection.channel()
# #     channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# #     def callback(ch, method, properties, body):
# #         event = json.loads(body)
# #         print("📥 Event received:", event)

# #         # HANDLE USER CREATED
# #         if event.get("event") == "USER_CREATED":
# #             Profile.objects.update_or_create(
# #                 auth_user_id=event["id"],
# #                 defaults={
# #                     "first_name": event.get("first_name", ""),
# #                     "last_name": event.get("last_name", ""),
# #                     "role": event.get("role", "client")
# #                 },
# #             )
# #             print(f"✅ USER_CREATED synced for user {event['id']}")

# #         # HANDLE USER UPDATED
# #         elif event.get("event") == "USER_UPDATED":
# #             Profile.objects.update_or_create(
# #                 auth_user_id=event["id"],
# #                 defaults={
# #                     "first_name": event.get("first_name", ""),
# #                     "last_name": event.get("last_name", ""),
# #                     "bio": event.get("bio", ""),
# #                     "location": event.get("location", ""),
# #                     "role": event.get("role", "client")
# #                 },
# #             )
# #             print(f"🔄 USER_UPDATED synced for user {event['id']}")

# #         ch.basic_ack(delivery_tag=method.delivery_tag)

# #     channel.basic_consume(
# #         queue=RABBITMQ_QUEUE,
# #         on_message_callback=callback,
# #         auto_ack=False
# #     )

# #     print("🟢 User Service RabbitMQ Consumer Listening…")
# #     channel.start_consuming()




# # import json
# # import pika
# # import os
# # from user_profile.models import Profile

# # RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# # RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


# # def start_consumer():
# #     connection = pika.BlockingConnection(
# #         pika.ConnectionParameters(host=RABBITMQ_HOST)
# #     )
# #     channel = connection.channel()
# #     channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# #     def callback(ch, method, properties, body):
# #         event = json.loads(body)
# #         event_type = event.get("event")

# #         print("📥 Event received:", event)

# #         # 1️⃣ USER CREATED → create profile shell
# #         if event_type == "USER_CREATED":
# #             Profile.objects.update_or_create(
# #                 auth_user_id=event["user_id"],
# #                 defaults={
# #                     "first_name": event.get("first_name", ""),
# #                     "last_name": event.get("last_name", ""),
# #                 },
# #             )
# #             print(f"✅ USER_CREATED handled for user {event['user_id']}")

# #         # 2️⃣ ROLE UPDATED → authoritative role sync
# #         elif event_type == "USER_ROLE_UPDATED":
# #             Profile.objects.update_or_create(
# #                 auth_user_id=event["user_id"],
# #                 defaults={
# #                     "role": event["role"],
# #                     "is_profession_verified": event.get("is_verified", True),
# #                 },
# #             )
# #             print(
# #                 f"🔐 USER_ROLE_UPDATED synced: "
# #                 f"user={event['user_id']} role={event['role']}"
# #             )

# #         else:
# #             print(f"⚠️ Ignored unknown event: {event_type}")

# #         ch.basic_ack(delivery_tag=method.delivery_tag)

# #     channel.basic_consume(
# #         queue=RABBITMQ_QUEUE,
# #         on_message_callback=callback,
# #         auto_ack=False,
# #     )

# #     print("🟢 Profile Service RabbitMQ Consumer listening…")
# #     channel.start_consuming()




# # import json
# # import os
# # import time
# # import pika
# # from user_profile.models import Profile

# # RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# # RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
# # RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
# # RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
# # RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")



# # def start_consumer():
# #     while True:
# #         try:
# #             print("🟡 Connecting to RabbitMQ...")
# #             credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

# #             connection = pika.BlockingConnection(
# #                 pika.ConnectionParameters(
# #                     host=RABBITMQ_HOST,
# #                     virtual_host=RABBITMQ_VHOST,
# #                     credentials=credentials,
# #                     heartbeat=600,
# #                     blocked_connection_timeout=300,
# #                 )
# #             )
# #             channel = connection.channel()
# #             channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# #             print("🟢 User Service RabbitMQ Consumer Listening…")

# #         def callback(ch, method, properties, body):
# #             event = json.loads(body)
# #             print("📥 Event received:", event)

# #             event_type = event.get("event")
# #             user_id = event.get("user_id")

# #             # USER CREATED
# #             if event_type == "USER_CREATED":
# #                 Profile.objects.update_or_create(
# #                     auth_user_id=user_id,
# #                     defaults={
# #                         "first_name": event.get("first_name", ""),
# #                         "last_name": event.get("last_name", ""),
# #                         "role": event.get("role", "client"),
# #                     },
# #                 )
# #                 print(f"✅ USER_CREATED synced for user {user_id}")

# #             # PROFILE UPDATED (bio, location, avatar, etc.)
# #             elif event_type == "PROFILE_UPDATED":
# #                 Profile.objects.filter(auth_user_id=user_id).update(
# #                     **event.get("changes", {})
# #                 )
# #                 print(f"🔄 PROFILE_UPDATED synced for user {user_id}")

# #             # 🔥 ROLE UPDATED (THIS WAS MISSING)
# #             elif event_type == "USER_ROLE_UPDATED":
# #                 Profile.objects.update_or_create(
# #                     auth_user_id=user_id,
# #                     defaults={
# #                         "role": event.get("role", "client"),
# #                     },
# #                 )
# #                 print(f"🛡️ USER_ROLE_UPDATED synced for user {user_id}")

# #             else:
# #                 print("⚠️ Unknown event type:", event_type)

# #             ch.basic_ack(delivery_tag=method.delivery_tag)


# #             channel.basic_consume(
# #                 queue=RABBITMQ_QUEUE,
# #                 on_message_callback=callback,
# #                 auto_ack=False,
# #             )

# #             channel.start_consuming()

# #         except Exception as e:
# #             print("🔴 RabbitMQ connection failed. Retrying in 5 seconds...")
# #             print(e)
# #             time.sleep(5)



# # import json
# # import os
# # import time
# # import pika
# # from user_profile.models import Profile

# # RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# # RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
# # RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
# # RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
# # RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


# # def start_consumer():
# #     while True:
# #         try:
# #             print("🟡 Connecting to RabbitMQ...")

# #             credentials = pika.PlainCredentials(
# #                 RABBITMQ_USER,
# #                 RABBITMQ_PASS
# #             )

# #             connection = pika.BlockingConnection(
# #                 pika.ConnectionParameters(
# #                     host=RABBITMQ_HOST,
# #                     virtual_host=RABBITMQ_VHOST,
# #                     credentials=credentials,
# #                     heartbeat=600,
# #                     blocked_connection_timeout=300,
# #                 )
# #             )

# #             channel = connection.channel()
# #             channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# #             print("🟢 User Service RabbitMQ Consumer Listening…")

# #             def callback(ch, method, properties, body):
# #                 event = json.loads(body)
# #                 print("📥 Event received:", event)

# #                 event_type = event.get("event")
# #                 user_id = event.get("user_id")

# #                 # USER CREATED
# #                 if event_type == "USER_CREATED":
# #                     Profile.objects.get_or_create(
# #                         auth_user_id=event["user_id"],
# #                         defaults={
# #                             "first_name": event.get("first_name", ""),
# #                             "last_name": event.get("last_name", ""),
                           
# #                         },
# #                     )


# #                 # PROFILE UPDATED
# #                 elif event_type == "PROFILE_UPDATED":
# #                     changes = event.get("changes", {})
# #                     changes.pop("role", None)  # 🔥 safety guard

# #                     Profile.objects.filter(auth_user_id=user_id).update(**changes)


# #                 # ROLE UPDATED
# #                 elif event_type == "USER_ROLE_UPDATED":
# #                     Profile.objects.filter(auth_user_id=user_id).update(
# #                         role=event["role"]
# #                     )
# #                     print(f"✅ Role updated for user {user_id}")


# #                 else:
# #                     print("⚠️ Unknown event type:", event_type)

# #                 ch.basic_ack(delivery_tag=method.delivery_tag)

# #             channel.basic_consume(
# #                 queue=RABBITMQ_QUEUE,
# #                 on_message_callback=callback,
# #                 auto_ack=False,
# #             )

# #             channel.start_consuming()

# #         except Exception as e:
# #             print("🔴 RabbitMQ connection failed. Retrying in 5 seconds...")
# #             print(e)
# #             time.sleep(5)




# # import json
# # import os
# # import time
# # import pika
# # from user_profile.models import Profile



# # RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# # RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
# # RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
# # RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


# # def start():
# #     while True:
# #         try:
# #             print("🟡 Connecting to RabbitMQ...")
# #             creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
# #             connection = pika.BlockingConnection(
# #                 pika.ConnectionParameters(
# #                     host=RABBITMQ_HOST,
# #                     credentials=creds,
# #                 )
# #             )

# #             channel = connection.channel()
# #             channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# #             print("🟢 User Service consuming user_events")

# #             def callback(ch, method, properties, body):
# #                 event = json.loads(body)
# #                 print("📥 RECEIVED EVENT:", event)

# #                 if event.get("event") == "USER_ROLE_UPDATED":
# #                     Profile.objects.update_or_create(
# #                         auth_user_id=event["user_id"],
# #                         defaults={"role": event["role"]},
# #                     )
# #                     print(f"✅ Role updated for user {event['user_id']}")


# #                 ch.basic_ack(delivery_tag=method.delivery_tag)

# #             channel.basic_consume(
# #                 queue=RABBITMQ_QUEUE,
# #                 on_message_callback=callback,
# #             )

# #             channel.start_consuming()

# #         except Exception as e:
# #             print("🔴 Consumer crashed, retrying in 5s", e)
# #             time.sleep(5)




import json
import os
import time
import pika
from user_profile.models import Profile

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")


def start_consumer():
    while True:
        try:
            print("🟡 Connecting to RabbitMQ...")

            creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    credentials=creds,
                )
            )

            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

            print("🟢 User Service consuming user_events")

            def callback(ch, method, properties, body):
                event = json.loads(body)
                event_type = event.get("event")
                user_id = event.get("user_id")

                if event_type == "USER_CREATED":
                    Profile.objects.update_or_create(
                        auth_user_id=user_id,
                        defaults={
                            "first_name": event.get("first_name", ""),
                            "last_name": event.get("last_name", ""),
                            "role": event.get("role", "client"),
                        },
                    )
                    print(f"✅ USER_CREATED synced for user {user_id}")

                elif event_type == "USER_ROLE_UPDATED":
                    Profile.objects.update_or_create(
                        auth_user_id=user_id,
                        defaults={"role": event["role"]},
                    )
                    print(f"✅ Role updated for user {user_id}")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue=RABBITMQ_QUEUE,
                on_message_callback=callback,
                auto_ack=False,
            )

            channel.start_consuming()

        except Exception as e:
            print("🔴 Consumer crashed, retrying in 5s", e)
            time.sleep(5)
