from bson import ObjectId
from django.conf import settings

from core.mongo import get_mongo_db


COLLECTION_NAME = 'transcriptions'


def get_collection():
    return get_mongo_db()[COLLECTION_NAME]


def serialize_transcription(document):
    return {
        'id': str(document.get('_id')),
        'title': document.get('title'),
        'text': document.get('text'),
        'folder': document.get('folder'),
        'topics': document.get('topics', []),
        'created_at': document.get('created_at'),
        'length_sec': document.get('length_sec'),
        'speakers': document.get('speakers', []),
    }


def parse_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except Exception as exc:  # noqa: BLE001
        raise ValueError('Invalid transcription id.') from exc
