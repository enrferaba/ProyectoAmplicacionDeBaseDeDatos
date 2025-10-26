import time
from typing import Any, Dict

from django.conf import settings
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class CachePingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        key = 'cache:ping'
        data: Dict[str, Any] | None = cache.get(key)
        if not data:
            start = time.perf_counter()
            total = sum(i * i for i in range(100000))
            elapsed = (time.perf_counter() - start) * 1000
            data = {
                'message': 'Cache miss - recomputed expensive operation',
                'duration_ms': round(elapsed, 2),
                'result': total,
            }
            cache.set(key, data, timeout=settings.CACHE_PING_TTL)
        else:
            data = {
                **data,
                'message': 'Cache hit',
            }
        return Response(data)
