from dataclasses import dataclass

from django.conf import settings

from .redis import get_redis_connection


@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    ttl: int


class RedisRateLimiter:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.client = get_redis_connection()

    def _key(self, identifier: str) -> str:
        return f"rl:{self.prefix}:{identifier}"

    def allow(self, identifier: str, limit: int, window: int) -> RateLimitResult:
        key = self._key(identifier)
        pipeline = self.client.pipeline()
        pipeline.incr(key, 1)
        pipeline.ttl(key)
        count, ttl = pipeline.execute()
        if ttl == -1:
            self.client.expire(key, window)
            ttl = window
        allowed = count <= limit
        remaining = max(limit - count, 0)
        return RateLimitResult(allowed=allowed, remaining=remaining, ttl=ttl)


login_rate_limiter = RedisRateLimiter('login')
otp_rate_limiter = RedisRateLimiter('otp')

