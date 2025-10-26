from unittest.mock import MagicMock, patch

import mongomock
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from fakeredis import FakeRedis


class TranscriptionCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(username='tester', password='pass1234')
        self.client.force_authenticate(user)
        self.collection = mongomock.MongoClient().db.collection
        self.redis = FakeRedis(decode_responses=True)
        self.channel_layer = MagicMock()
        self.patches = [
            patch('transcripts.views.get_collection', return_value=self.collection),
            patch('transcripts.views.get_redis_connection', return_value=self.redis),
            patch('transcripts.views.publish'),
            patch('transcripts.views.get_channel_layer', return_value=self.channel_layer),
        ]
        for p in self.patches:
            p.start()
        self.addCleanup(lambda: [p.stop() for p in self.patches])

    def test_crud_flow(self):
        payload = {
            'title': 'Test',
            'text': 'Lorem ipsum',
            'folder': 'docs',
            'topics': ['ai'],
            'length_sec': 120,
            'speakers': ['Alice'],
        }
        response = self.client.post('/transcriptions/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        transcription_id = response.data['id']

        response = self.client.get('/transcriptions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(f'/transcriptions/{transcription_id}')
        self.assertEqual(response.status_code, 200)

        update_payload = {**payload, 'title': 'Updated'}
        response = self.client.put(f'/transcriptions/{transcription_id}', update_payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated')

        response = self.client.delete(f'/transcriptions/{transcription_id}')
        self.assertEqual(response.status_code, 204)
