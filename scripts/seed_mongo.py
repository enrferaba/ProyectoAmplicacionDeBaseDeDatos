import random
from datetime import datetime, timedelta

from faker import Faker
from pymongo import MongoClient

from dotenv import load_dotenv
import os

load_dotenv()

fake = Faker()

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.environ.get('MONGO_DB', 'abdb')

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db['transcriptions']

TOPICS = ['finance', 'ai', 'health', 'education', 'sports', 'politics', 'music', 'science']


def main():
    collection.delete_many({})
    for _ in range(20):
        created_at = datetime.utcnow() - timedelta(days=random.randint(0, 14))
        doc = {
            'title': fake.sentence(),
            'text': fake.paragraph(nb_sentences=5),
            'folder': random.choice(['general', 'meetings', 'webinars']),
            'topics': random.sample(TOPICS, k=random.randint(1, 3)),
            'created_at': created_at,
            'length_sec': random.randint(60, 3600),
            'speakers': [fake.name() for _ in range(random.randint(1, 4))],
        }
        collection.insert_one(doc)
    print('Seeded MongoDB with 20 transcriptions')


if __name__ == '__main__':
    main()
