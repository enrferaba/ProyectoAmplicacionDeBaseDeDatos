from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.mongo import get_mongo_db


class DashboardSummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db = get_mongo_db()
        collection = db['transcriptions']
        since = datetime.utcnow() - timedelta(days=settings.DASHBOARD_DAYS)

        per_day = list(
            collection.aggregate(
                [
                    {'$match': {'created_at': {'$gte': since}}},
                    {
                        '$group': {
                            '_id': {
                                '$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}
                            },
                            'count': {'$sum': 1},
                        }
                    },
                    {'$sort': {'_id': 1}},
                ]
            )
        )

        top_topics = list(
            collection.aggregate(
                [
                    {'$unwind': '$topics'},
                    {'$group': {'_id': '$topics', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}},
                    {'$limit': 10},
                ]
            )
        )

        avg_length = list(
            collection.aggregate(
                [
                    {
                        '$group': {
                            '_id': None,
                            'average': {'$avg': '$length_sec'},
                            'speakers': {'$addToSet': '$speakers'},
                        }
                    }
                ]
            )
        )

        average_duration = avg_length[0]['average'] if avg_length else 0
        speaker_sets = avg_length[0]['speakers'] if avg_length else []
        distinct_speakers = len({speaker for speakers in speaker_sets for speaker in speakers})

        return Response(
            {
                'per_day': per_day,
                'top_topics': top_topics,
                'average_duration': average_duration,
                'distinct_speakers': distinct_speakers,
            }
        )


class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'dashboards/index.html')
