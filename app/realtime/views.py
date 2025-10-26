from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.redis import get_redis_connection


class RealtimeCounterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client = get_redis_connection()
        value = client.get('realtime:transcriptions_count')
        return Response({'count': int(value) if value else 0})
