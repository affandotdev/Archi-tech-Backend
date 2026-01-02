import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)

ONLINE_USERS_KEY = "chat:online_users"


def user_online(user_id: str):
    redis_client.sadd(ONLINE_USERS_KEY, user_id)


def user_offline(user_id: str):
    redis_client.srem(ONLINE_USERS_KEY, user_id)


def is_user_online(user_id: str) -> bool:
    return redis_client.sismember(ONLINE_USERS_KEY, user_id)
