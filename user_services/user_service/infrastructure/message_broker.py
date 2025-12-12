import json
import os
import logging
import pika

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "admin")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "user_events")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")


def _get_connection():
    creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VHOST,
        credentials=creds,
        heartbeat=600,
        blocked_connection_timeout=300,
    )
    return pika.BlockingConnection(params)


def publish_message(message: dict):
    try:
        conn = _get_connection()
        ch = conn.channel()
        ch.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        ch.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
            ),
        )

        logger.info(f"📤 Published: {message}")
        conn.close()
    except Exception as e:
        logger.exception(f"❌ Failed to publish: {message}")


def publish_profile_updated(user_id, data: dict):
    message = {
        "event": "PROFILE_UPDATED",
        "id": user_id,
        **data
    }
    publish_message(message)
