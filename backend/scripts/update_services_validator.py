"""
Update the MongoDB 'services' collection validator to a permissive JSON Schema
so API inserts are not blocked by legacy required fields.

This script will:
- Print the current validator for 'services'
- Apply a new validator that enforces basic types but has no `required` list
  and sets `validationLevel` to 'moderate' and `validationAction` to 'warn'

Run:
  python scripts/update_services_validator.py

Make a backup or run in a safe environment first if you have production data.
"""

from pymongo import MongoClient
import os
import pprint

MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'electrofixdb')

client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]

print('Connecting to', MONGODB_URI, 'db:', MONGODB_NAME)

# Read current collection options
try:
    info = db.command('listCollections', filter={'name': 'services'})
    coll_info = info.get('cursor', {}).get('firstBatch', [])
    if coll_info:
        current_opts = coll_info[0].get('options', {})
        print('\nCurrent services collection options:')
        pprint.pprint(current_opts)
    else:
        print('\nNo existing services collection metadata found (collection may be empty).')
except Exception as e:
    print('Failed to list collection info:', e)

# Define a permissive validator: basic type hints, but NO required fields
new_validator = {
    '$jsonSchema': {
        'bsonType': 'object',
        'properties': {
            'name': { 'bsonType': 'string' },
            'description': { 'bsonType': 'string' },
            'price': { 'bsonType': ['int', 'double', 'long', 'decimal'] },
            'duration': { 'bsonType': ['int', 'long'] },
            'category': { 'bsonType': 'string' },
            'image': { 'bsonType': 'string' },
            'features': { 'bsonType': 'array' },
            'is_active': { 'bsonType': 'bool' },
            'created_at': { 'bsonType': 'date' },
            'updated_at': { 'bsonType': 'date' },
            # keep placeholders for legacy fields but don't require them
            'fieldname1': { 'bsonType': 'string' },
            'fieldname2': { 'bsonType': ['int', 'long'] }
        },
        'additionalProperties': True
    }
}

print('\nApplying new validator (validationLevel=moderate, validationAction=warn) ...')
try:
    res = db.command({
        'collMod': 'services',
        'validator': new_validator,
        'validationLevel': 'moderate',
        'validationAction': 'warn'
    })
    print('collMod result:')
    pprint.pprint(res)
    print('\nNew validator applied. Inserts will no longer be blocked by missing legacy required fields; violations will be warned.')
except Exception as e:
    print('Failed to apply collMod:', e)
    print('As a fallback, attempt to create the collection with the validator if it does not exist.')
    try:
        db.create_collection('services')
        db.command({
            'collMod': 'services',
            'validator': new_validator,
            'validationLevel': 'moderate',
            'validationAction': 'warn'
        })
        print('Created services collection and applied validator.')
    except Exception as e2:
        print('Fallback failed:', e2)

print('\nDone.')
