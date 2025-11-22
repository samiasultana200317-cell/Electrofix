import os
import sys

print('=== Testing Django Basic Setup ===')
print(f'Current directory: {os.getcwd()}')
print(f'Python path: {sys.executable}')

# Check if we can import Django
try:
    import django
    print(f'✅ Django version: {django.__version__}')
except ImportError as e:
    print(f'❌ Django import failed: {e}')
    sys.exit(1)

# Check settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrofix_project.settings')
    django.setup()
    print('✅ Django setup successful')
    
    from django.conf import settings
    print(f'✅ Settings loaded: {settings.DEBUG}')
    
except Exception as e:
    print(f'❌ Django setup failed: {e}')
    import traceback
    traceback.print_exc()

print('=== Basic Setup Test Complete ===')
