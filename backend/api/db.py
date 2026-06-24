from django.conf import settings
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


_client = None


def get_database():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=900)
    return _client[settings.MONGODB_DATABASE]


def mongo_available():
    try:
        get_database().command("ping")
        return True
    except (PyMongoError, ServerSelectionTimeoutError):
        return False
