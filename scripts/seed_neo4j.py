import os
import random

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'neo4jpass')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

TRANSCRIPTIONS = [
    {'id': 't1', 'title': 'AI Trends 2024', 'topics': ['ai', 'technology']},
    {'id': 't2', 'title': 'Healthcare Innovations', 'topics': ['health', 'science']},
    {'id': 't3', 'title': 'Financial Markets', 'topics': ['finance', 'economy']},
    {'id': 't4', 'title': 'Sports Weekly', 'topics': ['sports']},
    {'id': 't5', 'title': 'Music and Culture', 'topics': ['music', 'culture']},
]

USERS = [
    {'id': 'u1', 'name': 'Alice'},
    {'id': 'u2', 'name': 'Bob'},
    {'id': 'u3', 'name': 'Carol'},
    {'id': 'u4', 'name': 'Dave'},
    {'id': 'u5', 'name': 'Eve'},
]


def seed():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.run("""
        CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;
        CREATE CONSTRAINT tr_id IF NOT EXISTS FOR (t:Transcription) REQUIRE t.id IS UNIQUE;
        CREATE CONSTRAINT tp_name IF NOT EXISTS FOR (tp:Topic) REQUIRE tp.name IS UNIQUE;
        """)
        for transcription in TRANSCRIPTIONS:
            session.run(
                "MERGE (t:Transcription {id: $id, title: $title})",
                transcription,
            )
            for topic in transcription['topics']:
                session.run(
                    "MERGE (tp:Topic {name: $name})",
                    {'name': topic},
                )
                session.run(
                    "MATCH (t:Transcription {id: $id}), (tp:Topic {name: $name}) MERGE (t)-[:HAS_TOPIC]->(tp)",
                    {'id': transcription['id'], 'name': topic},
                )
        for user in USERS:
            session.run("MERGE (u:User {id: $id, name: $name})", user)
        for user in USERS:
            listened = random.sample(TRANSCRIPTIONS, k=random.randint(1, len(TRANSCRIPTIONS)))
            for transcription in listened:
                session.run(
                    "MATCH (u:User {id: $uid}), (t:Transcription {id: $tid}) MERGE (u)-[:LISTENED_TO {weight: $weight, ts: timestamp()}]->(t)",
                    {'uid': user['id'], 'tid': transcription['id'], 'weight': random.randint(1, 5)},
                )
    print('Seeded Neo4j with sample data')


if __name__ == '__main__':
    seed()
