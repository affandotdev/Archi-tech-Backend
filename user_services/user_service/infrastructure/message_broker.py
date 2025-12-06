import json
import threading
import pika
import os


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")



def handle_user_created_event(data):
    from user_profile.models import Profile
    import traceback

    try:
        auth_user_id = data.get("id")
        if not auth_user_id:
            print("❌ Error: Missing user ID in event data")
            return

        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        role = data.get("role", "client")

        # Use update_or_create to avoid duplicates and update existing profiles
        profile, created = Profile.objects.update_or_create(
            auth_user_id=auth_user_id,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
            }
        )

        action = "created" if created else "updated"
        print(f"✅ Profile {action} for user {auth_user_id} with role: {role}")
    except Exception as e:
        print(f"❌ Error handling user created event: {str(e)}")
        traceback.print_exc()


def start_user_created_consumer():
    def run():
        while True:
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
                channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

                print("🟢 RabbitMQ consumer listening…")

                def callback(ch, method, properties, body):
                    data = json.loads(body.decode())
                    print("📥 Event received:", data)

                    if data.get("event") == "USER_CREATED":
                        handle_user_created_event(data)

                channel.basic_consume(
                    queue=RABBITMQ_QUEUE,
                    on_message_callback=callback,
                    auto_ack=True
                )

                channel.start_consuming()

            except Exception as e:
                print("❌ Consumer crashed, retrying…", str(e))

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
