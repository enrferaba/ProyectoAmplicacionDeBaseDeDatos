import random
from dataclasses import dataclass

from django.conf import settings

from .rate_limit import otp_rate_limiter
from .redis import get_redis_connection


@dataclass
class OTPResult:
    code: str
    ttl: int


class OTPService:
    def __init__(self) -> None:
        self.client = get_redis_connection()

    def _otp_key(self, user_id: int) -> str:
        return f"otp:{user_id}"

    def _attempts_key(self, user_id: int) -> str:
        return f"otp:attempts:{user_id}"

    def generate(self, user_id: int) -> OTPResult:
        limiter = otp_rate_limiter.allow(
            identifier=f"request:{user_id}",
            limit=settings.RATE_LIMIT_OTP_REQUEST,
            window=settings.OTP_WINDOW_SECONDS,
        )
        if not limiter.allowed:
            raise ValueError('OTP request limit reached, try again later.')
        code = f"{random.randint(0, 999999):06d}"
        key = self._otp_key(user_id)
        self.client.setex(key, settings.OTP_TTL_SECONDS, code)
        self.client.delete(self._attempts_key(user_id))
        return OTPResult(code=code, ttl=settings.OTP_TTL_SECONDS)

    def verify(self, user_id: int, code: str) -> bool:
        attempts_key = self._attempts_key(user_id)
        attempts = self.client.incr(attempts_key, 1)
        if attempts == 1:
            self.client.expire(attempts_key, settings.OTP_WINDOW_SECONDS)
        if attempts > settings.OTP_MAX_ATTEMPTS:
            raise ValueError('Maximum OTP attempts exceeded.')
        stored_code = self.client.get(self._otp_key(user_id))
        if stored_code and stored_code == code:
            self.client.delete(self._otp_key(user_id))
            self.client.delete(attempts_key)
            return True
        return False


otp_service = OTPService()
