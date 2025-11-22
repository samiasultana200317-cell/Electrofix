from pymongo import MongoClient
import os

uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
db_name = os.environ.get('MONGODB_NAME', 'electrofixdb')
client = MongoClient(uri)
db = client[db_name]
print('Collections:', db.list_collection_names())
for name in ['services','bookings','users','technicians']:
    if name in db.list_collection_names():
        print('\n==', name, 'sample docs ==')
        for d in db[name].find().limit(5):
            print(d)
    else:
        print('\n==', name, 'collection not present ==')
