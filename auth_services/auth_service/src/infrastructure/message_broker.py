# rabbit_publisher.py
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
        blocked_connection_timeout=300
    )
    return pika.BlockingConnection(params)

def publish_message(message: dict):
    try:
        conn = _get_connection()
        ch = conn.channel()
        # ensure queue exists and is durable
        ch.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        # make message persistent (delivery_mode=2)
        ch.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(content_type='application/json', delivery_mode=2)
        )
        logger.info("Published event to %s: %s", RABBITMQ_QUEUE, message)
        conn.close()
    except Exception:
        logger.exception("Failed to publish message: %s", message)

def publish_user_updated_event(user_id, data: dict):
    SAFE_FIELDS = {
        "first_name",
        "last_name",
        "bio",
        "location",
        "avatar_url",
    }

    clean_data = {k: v for k, v in data.items() if k in SAFE_FIELDS}

    message = {
        "event": "PROFILE_UPDATED",
        "user_id": user_id,
        "changes": clean_data,
    }
    publish_message(message)


# def publish_user_updated_event(user_id, data: dict):
#     message = {
#         "event": "PROFILE_UPDATED",
#         "id": user_id,
#         **data
#     }
#     publish_message(message)



def publish_user_role_updated_event(user_id, role, is_verified=True):
    message = {
        "event": "USER_ROLE_UPDATED",
        "user_id": user_id,
        "role": role,
        "is_verified": is_verified,
    }
    publish_message(message)


def publish_user_created_event(user_id, email, username, first_name, role, last_name):
    message = {
        "event": "USER_CREATED",
        "user_id": user_id,
        "email": email,
        "username": username,
        "first_name": first_name,
        "role": role,
        "last_name": last_name
    }
    publish_message(message)


