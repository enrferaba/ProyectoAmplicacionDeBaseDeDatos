from django.test import TestCase
from fakeredis import FakeRedis

from core import otp
from core import rate_limit


class OTPServiceTests(TestCase):
    def setUp(self):
        self.redis = FakeRedis(decode_responses=True)
        otp.otp_service.client = self.redis
        rate_limit.otp_rate_limiter.client = self.redis

    def test_generate_and_verify(self):
        result = otp.otp_service.generate(1)
        self.assertEqual(len(result.code), 6)
        verified = otp.otp_service.verify(1, result.code)
        self.assertTrue(verified)

    def test_block_after_max_attempts(self):
        otp.otp_service.generate(2)
        for _ in range(3):
            otp.otp_service.verify(2, '000000')
        with self.assertRaises(ValueError):
            otp.otp_service.verify(2, '000000')
