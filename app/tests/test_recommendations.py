from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient


class RecommendationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('recommender.views.run_query')
    def test_content_recommendations(self, run_query):
        run_query.return_value = iter([
            {'id': 't2', 'title': 'Second', 'score': 3},
            {'id': 't3', 'title': 'Third', 'score': 1},
        ])
        response = self.client.get('/reco/content/u1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    @patch('recommender.views.run_query')
    def test_hybrid_combines_scores(self, run_query):
        def side_effect(query, params):
            if 'count(tp)' in query.lower():
                return iter([
                    {'id': 't2', 'title': 'Second', 'score': 4},
                ])
            return iter([
                {'id': 't3', 'title': 'Third', 'score': 2},
            ])

        run_query.side_effect = side_effect
        response = self.client.get('/reco/hybrid/u1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], 't2')
