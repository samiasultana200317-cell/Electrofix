from pymongo import MongoClient, errors
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MongoDBManager:
    _client = None
    _db = None
    _connected = False

    @classmethod
    def get_client(cls):
        """Return a cached MongoClient. Does a lightweight ping once. Never raises at import time."""
        if cls._client is None:
            try:
                cls._client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
                # Test connection (ismaster deprecated; use ping)
                cls._client.admin.command('ping')
                cls._connected = True
            except errors.PyMongoError as e:
                logger.warning(f"MongoDB connection failed: {e}")
                cls._connected = False
        return cls._client

    @classmethod
    def is_connected(cls):
        """Returns True if last connection attempt succeeded."""
        # Ensure we attempted at least once
        cls.get_client()
        return cls._connected

    @classmethod
    def get_db(cls):
        if cls._db is None:
            client = cls.get_client()
            if not cls._connected or client is None:
                raise RuntimeError("MongoDB not available. Ensure the server is running on MONGODB_URI.")
            cls._db = client[settings.MONGODB_NAME]
        return cls._db

    @classmethod
    def get_collection(cls, collection_name):
        db = cls.get_db()
        return db[collection_name]

# Collections
def get_users_collection():
    return MongoDBManager.get_collection('users')

def get_services_collection():
    return MongoDBManager.get_collection('services')

def get_bookings_collection():
    return MongoDBManager.get_collection('bookings')

def get_technicians_collection():
    return MongoDBManager.get_collection('technicians')

def get_orders_collection():
    return MongoDBManager.get_collection('orders')

def get_connection_status():
    """Helper for diagnostics endpoints to report connection status."""
    return {
        "connected": MongoDBManager.is_connected(),
        "uri": settings.MONGODB_URI,
        "db": settings.MONGODB_NAME,
    }
