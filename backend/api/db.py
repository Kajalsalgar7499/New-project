import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/foodexpress")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "foodexpress")

_client = None


def get_database():
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=900)
    return _client[MONGODB_DATABASE]


def mongo_available():
    try:
        get_database().command("ping")
        return True
    except (PyMongoError, ServerSelectionTimeoutError):
        return False
