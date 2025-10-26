from typing import Dict, List

from neo4j.exceptions import Neo4jError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.neo4j import run_query


LISTEN_QUERY = """
MERGE (u:User {id: $user_id})
ON CREATE SET u.name = coalesce($user_name, $user_id)
WITH u
MATCH (t:Transcription {id: $transcription_id})
MERGE (u)-[rel:LISTENED_TO]->(t)
ON CREATE SET rel.weight = coalesce($weight, 1), rel.ts = timestamp()
ON MATCH SET rel.weight = coalesce($weight, rel.weight), rel.ts = timestamp()
RETURN u.id AS user_id, t.id AS transcription_id
"""

CONTENT_QUERY = """
MATCH (u:User {id:$user_id})-[:LISTENED_TO]->(:Transcription)-[:HAS_TOPIC]->(tp:Topic)<-[:HAS_TOPIC]-(t2:Transcription)
WHERE NOT (u)-[:LISTENED_TO]->(t2)
RETURN t2.id AS id, t2.title AS title, count(tp) AS score
ORDER BY score DESC LIMIT 5
"""

COLLAB_QUERY = """
MATCH (u:User {id:$user_id})-[:LISTENED_TO]->(t:Transcription)<-[:LISTENED_TO]-(u2:User)
WHERE u2 <> u
WITH u, u2, count(t) AS inter
ORDER BY inter DESC LIMIT 10
MATCH (u2)-[:LISTENED_TO]->(cand:Transcription)
WHERE NOT (u)-[:LISTENED_TO]->(cand)
RETURN cand.id AS id, cand.title AS title, count(*) AS score
ORDER BY score DESC LIMIT 5
"""

SIMILAR_USERS_QUERY = """
MATCH (u:User {id:$user_id})-[:LISTENED_TO]->(:Transcription)<-[:LISTENED_TO]-(candidate:User)
WHERE u <> candidate
RETURN candidate.id AS id, count(*) AS weight
ORDER BY weight DESC LIMIT 5
"""

COMMUNITY_QUERY = """
CALL {
    WITH $graph_name AS graph_name
    CALL gds.graph.exists(graph_name) YIELD exists
    WITH graph_name, exists
    CALL apoc.do.when(exists,
        'CALL gds.graph.drop($graph_name) YIELD graphName RETURN graphName',
        'RETURN null as graphName',
        {graph_name: graph_name}) YIELD value
    RETURN 1
}
CALL gds.graph.project(
    $graph_name,
    'User',
    {
        LISTENED_TO: {
            orientation: 'UNDIRECTED'
        }
    }
)
YIELD graphName
CALL gds.louvain.stream(graphName)
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).id AS user_id, communityId
ORDER BY communityId
"""


class ListenEventView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        transcription_id = request.data.get('transcription_id')
        weight = request.data.get('weight', 1)
        if not user_id or not transcription_id:
            return Response({'detail': 'user_id and transcription_id are required.'}, status=400)
        try:
            list(
                run_query(
                    LISTEN_QUERY,
                    {
                        'user_id': str(user_id),
                        'user_name': request.data.get('user_name'),
                        'transcription_id': str(transcription_id),
                        'weight': weight,
                    },
                )
            )
        except Neo4jError as exc:
            return Response({'detail': str(exc)}, status=500)
        return Response({'message': 'Listen relationship stored.'})


class ContentRecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: str):
        recommendations = list(run_query(CONTENT_QUERY, {'user_id': user_id}))
        return Response(recommendations)


class CollaborativeRecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: str):
        recommendations = list(run_query(COLLAB_QUERY, {'user_id': user_id}))
        return Response(recommendations)


class HybridRecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: str):
        content = list(run_query(CONTENT_QUERY, {'user_id': user_id}))
        collab = list(run_query(COLLAB_QUERY, {'user_id': user_id}))

        def normalise(items: List[Dict[str, float]]) -> Dict[str, float]:
            if not items:
                return {}
            max_score = max(item['score'] for item in items)
            if max_score == 0:
                return {item['id']: 0.0 for item in items}
            return {item['id']: item['score'] / max_score for item in items}

        content_scores = normalise(content)
        collab_scores = normalise(collab)
        ids = set(content_scores) | set(collab_scores)
        output = []
        for item_id in ids:
            combined_score = content_scores.get(item_id, 0) + collab_scores.get(item_id, 0)
            title = next((item['title'] for item in content if item['id'] == item_id), None)
            if not title:
                title = next((item['title'] for item in collab if item['id'] == item_id), '')
            output.append({'id': item_id, 'title': title, 'score': round(combined_score, 3)})
        output.sort(key=lambda item: item['score'], reverse=True)
        return Response(output)


class SimilarUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: str):
        users = list(run_query(SIMILAR_USERS_QUERY, {'user_id': user_id}))
        return Response(users)


class CommunityDetectionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        graph_name = request.query_params.get('graph_name', 'abdb_communities')
        try:
            result = list(run_query(COMMUNITY_QUERY, {'graph_name': graph_name}))
        except Neo4jError as exc:
            return Response({'detail': str(exc)}, status=500)
        return Response(result)
