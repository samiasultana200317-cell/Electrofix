import os
import django

print('=== Testing Django + MongoDB Integration ===')

try:
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrofix_project.settings')
    django.setup()
    print('✅ Django setup successful')
    
    # Test Django settings
    from django.conf import settings
    print(f'✅ Django settings loaded')
    print(f'   DEBUG: {settings.DEBUG}')
    print(f'   MONGODB_NAME: {settings.MONGODB_NAME}')
    
    # Test MongoDB through our manager
    from electrofix_app.mongodb import MongoDBManager
    print('✅ MongoDBManager imported in Django context')
    
    # Test database operations
    users_collection = MongoDBManager.get_collection('users')
    users_count = users_collection.count_documents({})
    print(f'✅ MongoDB operations working. Users count: {users_count}')
    
    # Test creating a sample user
    sample_user = {
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'customer'
    }
    result = users_collection.insert_one(sample_user)
    print(f'✅ Sample user created with ID: {result.inserted_id}')
    
    # Clean up
    users_collection.delete_one({'_id': result.inserted_id})
    print('✅ Sample user cleaned up')
    
except Exception as e:
    print(f'❌ Integration test failed: {e}')

print('=== Integration Test Complete ===')
