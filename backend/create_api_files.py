import os

# Create auth.py
auth_content = '''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..mongodb import get_users_collection

# Helper function to generate JWT token
def generate_token(user_id, email):
    payload = {
        'user_id': str(user_id),
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

# User Registration
@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'phone']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'{field} is required'
                }, status=400)
        
        users_collection = get_users_collection()
        
        # Check if user already exists
        if users_collection.find_one({'email': data['email']}):
            return JsonResponse({
                'success': False,
                'message': 'User with this email already exists'
            }, status=400)
        
        # Hash password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user document
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password,
            'phone': data['phone'],
            'address': data.get('address', {}),
            'role': 'customer',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        # Insert user into MongoDB
        result = users_collection.insert_one(user_data)
        
        # Generate token
        token = generate_token(result.inserted_id, data['email'])
        
        return JsonResponse({
            'success': True,
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': str(result.inserted_id),
                'name': data['name'],
                'email': data['email'],
                'phone': data['phone'],
                'role': 'customer'
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# User Login
@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return JsonResponse({
                'success': False,
                'message': 'Email and password are required'
            }, status=400)
        
        users_collection = get_users_collection()
        
        # Find user
        user = users_collection.find_one({'email': data['email']})
        if not user:
            return JsonResponse({
                'success': False,
                'message': 'Invalid email or password'
            }, status=401)
        
        # Check password
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            return JsonResponse({
                'success': False,
                'message': 'Invalid email or password'
            }, status=401)
        
        # Generate token
        token = generate_token(user['_id'], user['email'])
        
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'role': user.get('role', 'customer')
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Get User Profile
@require_http_methods(['GET'])
def get_profile(request):
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'success': False,
                'message': 'Authentication required'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        # Verify token
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'success': False,
                'message': 'Token expired'
            }, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid token'
            }, status=401)
        
        users_collection = get_users_collection()
        user = users_collection.find_one({'_id': user_id})
        
        if not user:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            }, status=404)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'role': user.get('role', 'customer'),
                'address': user.get('address', {})
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
'''

# Create services.py
services_content = '''
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..mongodb import get_services_collection

# Get all services
@require_http_methods(['GET'])
def get_services(request):
    try:
        services_collection = get_services_collection()
        services = list(services_collection.find({'is_active': True}))
        
        # Convert ObjectId to string and remove password fields
        for service in services:
            service['id'] = str(service['_id'])
            del service['_id']
        
        return JsonResponse({
            'success': True,
            'data': services
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Get service by ID
@require_http_methods(['GET'])
def get_service(request, service_id):
    try:
        services_collection = get_services_collection()
        service = services_collection.find_one({'_id': service_id})
        
        if not service:
            return JsonResponse({
                'success': False,
                'message': 'Service not found'
            }, status=404)
        
        service['id'] = str(service['_id'])
        del service['_id']
        
        return JsonResponse({
            'success': True,
            'data': service
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
'''

# Create bookings.py
bookings_content = '''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import jwt
from datetime import datetime
from django.conf import settings
from ..mongodb import get_bookings_collection, get_services_collection, get_users_collection

# Helper to get user from token
def get_user_from_token(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None

# Create booking
@csrf_exempt
@require_http_methods(['POST'])
def create_booking(request):
    try:
        user_id = get_user_from_token(request)
        if not user_id:
            return JsonResponse({
                'success': False,
                'message': 'Authentication required'
            }, status=401)
        
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['service_id', 'appliance_type', 'brand', 'model', 'problem_description', 'scheduled_date', 'time_slot', 'address']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'{field} is required'
                }, status=400)
        
        services_collection = get_services_collection()
        bookings_collection = get_bookings_collection()
        
        # Get service to calculate cost
        service = services_collection.find_one({'_id': data['service_id']})
        if not service:
            return JsonResponse({
                'success': False,
                'message': 'Service not found'
            }, status=404)
        
        # Create booking
        booking_data = {
            'user_id': user_id,
            'service_id': data['service_id'],
            'appliance_type': data['appliance_type'],
            'brand': data['brand'],
            'model': data['model'],
            'problem_description': data['problem_description'],
            'address': data['address'],
            'scheduled_date': datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00')),
            'time_slot': data['time_slot'],
            'status': 'pending',
            'total_cost': service['price'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = bookings_collection.insert_one(booking_data)
        
        return JsonResponse({
            'success': True,
            'message': 'Booking created successfully',
            'booking_id': str(result.inserted_id)
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Get user bookings
@require_http_methods(['GET'])
def get_user_bookings(request):
    try:
        user_id = get_user_from_token(request)
        if not user_id:
            return JsonResponse({
                'success': False,
                'message': 'Authentication required'
            }, status=401)
        
        bookings_collection = get_bookings_collection()
        services_collection = get_services_collection()
        
        # Get user's bookings
        bookings = list(bookings_collection.find({'user_id': user_id}).sort('created_at', -1))
        
        # Enrich booking data with service details
        enriched_bookings = []
        for booking in bookings:
            service = services_collection.find_one({'_id': booking['service_id']})
            
            enriched_booking = {
                'id': str(booking['_id']),
                'service_name': service['name'] if service else 'Unknown Service',
                'service_price': service['price'] if service else 0,
                'appliance_type': booking['appliance_type'],
                'brand': booking['brand'],
                'model': booking['model'],
                'problem_description': booking['problem_description'],
                'scheduled_date': booking['scheduled_date'].isoformat(),
                'time_slot': booking['time_slot'],
                'status': booking['status'],
                'total_cost': booking['total_cost'],
                'created_at': booking['created_at'].isoformat()
            }
            enriched_bookings.append(enriched_booking)
        
        return JsonResponse({
            'success': True,
            'data': enriched_bookings
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
'''

# Create updated urls.py
urls_content = '''
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.http import JsonResponse

# Import views
from electrofix_app.views.auth import register, login, get_profile
from electrofix_app.views.services import get_services, get_service
from electrofix_app.views.bookings import create_booking, get_user_bookings

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'ElectroFix Backend',
        'python_version': '3.14.0'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health check
    path('api/health/', health_check, name='health_check'),
    
    # Authentication
    path('api/auth/register/', register, name='register'),
    path('api/auth/login/', login, name='login'),
    path('api/auth/profile/', get_profile, name='profile'),
    
    # Services
    path('api/services/', get_services, name='get_services'),
    path('api/services/<str:service_id>/', get_service, name='get_service'),
    
    # Bookings
    path('api/bookings/', create_booking, name='create_booking'),
    path('api/bookings/my-bookings/', get_user_bookings, name='get_user_bookings'),
    
    # Frontend
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('pages/<path:page>', TemplateView.as_view(template_name='index.html'), name='frontend_pages'),
]
'''

# Write files
with open('electrofix_app/views/auth.py', 'w', encoding='utf-8') as f:
    f.write(auth_content)

with open('electrofix_app/views/services.py', 'w', encoding='utf-8') as f:
    f.write(services_content)

with open('electrofix_app/views/bookings.py', 'w', encoding='utf-8') as f:
    f.write(bookings_content)

with open('electrofix_project/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)

print('✅ All API files created successfully!')
print('✅ auth.py created')
print('✅ services.py created') 
print('✅ bookings.py created')
print('✅ urls.py updated')
