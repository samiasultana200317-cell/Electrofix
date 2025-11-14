import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

def create_jwt_token(user):
    payload = {
        'user_id': str(user._id),
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            token = auth_header.split(' ')[1]
            payload = decode_jwt_token(token)
            user = User.objects.get(_id=payload['user_id'])
            return (user, token)
        except (IndexError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token')

def get_user_from_request(request):
    return request.user