from datetime import datetime
from typing import List

from asgiref.sync import async_to_sync
from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

from channels.layers import get_channel_layer

from core.redis import get_redis_connection, publish
from .mongo import get_collection, parse_object_id, serialize_transcription
from .serializers import TranscriptionSerializer, TranscriptionUpdateSerializer


class TranscriptionListCreateView(APIView):
    def get(self, request):
        folder = request.query_params.get('folder')
        topics = request.query_params.getlist('topics') or request.query_params.get('topics')
        query = {}
        if folder:
            query['folder'] = folder
        if topics:
            if isinstance(topics, str):
                topics = [t.strip() for t in topics.split(',') if t.strip()]
            query['topics'] = {'$in': topics}
        documents = list(get_collection().find(query).sort('created_at', -1))
        return Response([serialize_transcription(doc) for doc in documents])

    def post(self, request):
        serializer = TranscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        payload['created_at'] = datetime.utcnow()
        result = get_collection().insert_one(payload)
        document = get_collection().find_one({'_id': result.inserted_id})
        serialized = serialize_transcription(document)
        redis_client = get_redis_connection()
        redis_client.incr('realtime:transcriptions_count', 1)
        publish('events:transcriptions', serialized['id'])
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'transcription_created',
                'data': {
                    'id': serialized['id'],
                    'title': serialized['title'],
                    'created_at': serialized['created_at'],
                },
            },
        )
        return Response(serialized, status=201)


class TranscriptionDetailView(APIView):
    def get_object(self, pk: str):
        try:
            object_id = parse_object_id(pk)
        except ValueError:
            return None
        document = get_collection().find_one({'_id': object_id})
        if not document:
            return None
        return document

    def get(self, request, pk: str):
        document = self.get_object(pk)
        if not document:
            return Response({'detail': 'Not found.'}, status=404)
        return Response(serialize_transcription(document))

    def put(self, request, pk: str):
        document = self.get_object(pk)
        if not document:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = TranscriptionUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_collection().update_one({'_id': document['_id']}, {'$set': serializer.validated_data})
        updated = get_collection().find_one({'_id': document['_id']})
        return Response(serialize_transcription(updated))

    def delete(self, request, pk: str):
        document = self.get_object(pk)
        if not document:
            return Response({'detail': 'Not found.'}, status=404)
        get_collection().delete_one({'_id': document['_id']})
        return Response(status=204)
