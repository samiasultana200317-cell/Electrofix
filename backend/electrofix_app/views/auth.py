
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..mongodb import get_users_collection
from bson import ObjectId
import uuid

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


# Forgot password - request a reset link (development: returns token in response)
@csrf_exempt
@require_http_methods(['POST'])
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email required'}, status=400)

        users_collection = get_users_collection()
        user = users_collection.find_one({'email': email})

        # Always return success to avoid leaking which emails exist.
        if not user:
            return JsonResponse({'success': True, 'message': 'If an account with that email exists, a reset link has been sent.'})

        # Create a reset token and expiry
        token = uuid.uuid4().hex
        expires = datetime.utcnow() + timedelta(hours=1)
        users_collection.update_one({'_id': user['_id']}, {'$set': {'reset_token': token, 'reset_expires': expires}})

        # In production: send email with token link. For dev, include token in response to allow testing.
        return JsonResponse({'success': True, 'message': 'Reset token generated (dev).', 'token': token})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def reset_password(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        new_password = data.get('password')
        if not token or not new_password:
            return JsonResponse({'success': False, 'message': 'Token and new password required'}, status=400)

        users_collection = get_users_collection()
        user = users_collection.find_one({'reset_token': token})
        if not user:
            return JsonResponse({'success': False, 'message': 'Invalid token'}, status=400)

        # Check expiry
        expires = user.get('reset_expires')
        if not expires or (isinstance(expires, str) and expires < datetime.utcnow().isoformat()):
            return JsonResponse({'success': False, 'message': 'Token expired'}, status=400)
        if isinstance(expires, datetime) and expires < datetime.utcnow():
            return JsonResponse({'success': False, 'message': 'Token expired'}, status=400)

        # Hash and update password
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        users_collection.update_one({'_id': user['_id']}, {'$set': {'password': hashed}, '$unset': {'reset_token': '', 'reset_expires': ''}})

        return JsonResponse({'success': True, 'message': 'Password reset successful'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

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
        try:
            oid = ObjectId(user_id)
        except Exception:
            return JsonResponse({'success': False, 'message': 'Invalid user id'}, status=400)
        user = users_collection.find_one({'_id': oid})
        
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


# Combined profile view to support GET (fetch) and PUT (update)
@csrf_exempt
@require_http_methods(['GET', 'PUT'])
def profile(request):
    # Delegate GET to existing get_profile behavior
    if request.method == 'GET':
        return get_profile(request)

    # Handle PUT -> update profile
    try:
        # Ensure Authorization header present
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'success': False, 'message': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'success': False, 'message': 'Invalid token'}, status=401)

        try:
            oid = ObjectId(user_id)
        except Exception:
            return JsonResponse({'success': False, 'message': 'Invalid user id'}, status=400)

        data = json.loads(request.body or '{}')
        users_collection = get_users_collection()

        update_fields = {}
        if 'name' in data:
            update_fields['name'] = data.get('name')
        if 'phone' in data:
            update_fields['phone'] = data.get('phone')
        if 'address' in data:
            update_fields['address'] = data.get('address')

        if update_fields:
            users_collection.update_one({'_id': oid}, {'$set': update_fields})

        updated = users_collection.find_one({'_id': oid})
        if not updated:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

        return JsonResponse({'success': True, 'message': 'Profile updated successfully', 'user': {
            'id': str(updated['_id']),
            'name': updated.get('name'),
            'email': updated.get('email'),
            'phone': updated.get('phone'),
            'address': updated.get('address', {})
        }})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
