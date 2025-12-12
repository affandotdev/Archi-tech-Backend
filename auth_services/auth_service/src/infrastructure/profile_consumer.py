import json
import pika
import threading
from django.conf import settings
from users.models import User

def handle_profile_updated(data):
    user_id = data.get("auth_user_id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    user = User.objects.filter(id=user_id).first()
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        print("✅ AUTH SERVICE UPDATED USER NAME")
    else:
        print("⚠️ User not found in auth service")

def run():
    def start():
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host="rabbitmq")
                )
                channel = connection.channel()

                channel.queue_declare(queue="profile_updates", durable=True)
                print("🟢 AUTH SERVICE LISTENING ON profile_updates")

                def callback(ch, method, properties, body):
                    event = json.loads(body.decode())
                    print("📥 RECEIVED:", event)

                    if event.get("event") == "PROFILE_UPDATED":
                        handle_profile_updated(event)

                    ch.basic_ack(delivery_tag=method.delivery_tag)

                channel.basic_consume(
                    queue="profile_updates",
                    on_message_callback=callback
                )

                channel.start_consuming()

            except Exception as e:
                print("❌ Consumer crashed:", e)

    thread = threading.Thread(target=start)
    thread.daemon = True
    thread.start()
