import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrofix_project.settings')
django.setup()

from electrofix_app.mongodb import MongoDBManager

print('=== Testing ElectroFix Setup with Python 3.14 ===')

# Test Django
try:
    from django.conf import settings
    print(f'✅ Django settings loaded: DEBUG={settings.DEBUG}')
except Exception as e:
    print(f'❌ Django settings error: {e}')

# Test MongoDB
try:
    client = MongoDBManager.get_client()
    db = MongoDBManager.get_db()
    print('✅ MongoDB connection successful')
    
    # Test basic operations
    users_collection = MongoDBManager.get_collection('users')
    users_count = users_collection.count_documents({})
    print(f'✅ MongoDB operations working. Users count: {users_count}')
    
except Exception as e:
    print(f'❌ MongoDB error: {e}')

print('=== Setup Test Complete ===')
