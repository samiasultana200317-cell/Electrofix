print('=== Testing Basic Imports ===')

try:
    import django
    print('✅ Django imported')
except ImportError as e:
    print(f'❌ Django import failed: {e}')

try:
    import pymongo
    print('✅ PyMongo imported')
except ImportError as e:
    print(f'❌ PyMongo import failed: {e}')

try:
    from decouple import config
    print('✅ python-decouple imported')
except ImportError as e:
    print(f'❌ python-decouple import failed: {e}')

try:
    from electrofix_app.mongodb import MongoDBManager
    print('✅ MongoDBManager imported successfully')
except ImportError as e:
    print(f'❌ MongoDBManager import failed: {e}')

print('=== Basic Import Test Complete ===')
