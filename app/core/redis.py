from functools import lru_cache
from typing import Any

import redis
from django.conf import settings


@lru_cache(maxsize=1)
def get_redis_connection() -> redis.Redis:
    return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def publish(channel: str, message: Any) -> None:
    client = get_redis_connection()
    client.publish(channel, message)
