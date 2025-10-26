from functools import lru_cache

from django.conf import settings
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    return MongoClient(settings.MONGO_URI)


def get_mongo_db():
    return get_mongo_client()[settings.MONGO_DB]
