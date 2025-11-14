from pymongo import MongoClient
from decouple import config

print('=== Testing MongoDB Connection ===')

try:
    # Get MongoDB settings
    mongodb_uri = config('MONGODB_URI', default='mongodb://localhost:27017/')
    mongodb_name = config('MONGODB_NAME', default='electrofix')
    
    print(f'Connecting to: {mongodb_uri}')
    print(f'Database: {mongodb_name}')
    
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    
    # Test connection
    client.admin.command('ismaster')
    print('✅ MongoDB connection successful!')
    
    # Test database access
    db = client[mongodb_name]
    collections = db.list_collection_names()
    print(f'✅ Database accessible. Collections: {collections}')
    
except Exception as e:
    print(f'❌ MongoDB connection failed: {e}')
    print('Please make sure MongoDB is running: net start MongoDB')

print('=== MongoDB Test Complete ===')
