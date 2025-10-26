import time

from django.test import TestCase, override_settings
from rest_framework.test import APIClient


@override_settings(
    CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
)
class CachePingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_cache_hit_is_fast(self):
        response1 = self.client.get('/cache/ping')
        self.assertEqual(response1.status_code, 200)
        start = time.perf_counter()
        response2 = self.client.get('/cache/ping')
        elapsed = (time.perf_counter() - start) * 1000
        self.assertEqual(response2.status_code, 200)
        self.assertLess(elapsed, 50)
        self.assertEqual(response2.data['message'], 'Cache hit')
