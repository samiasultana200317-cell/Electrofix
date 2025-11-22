import os
import sys
import traceback
from pymongo import MongoClient

uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
print('Using URI:', uri)
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    client.admin.command('ping')
    print('Mongo OK')
except Exception as e:
    print('Mongo error:', e)
    traceback.print_exc()
    sys.exit(1)
