import jwt
from django.conf import settings
from django.http import JsonResponse
from electrofix_app.models.user import User

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        user = User.objects.get(_id=user_id)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None

class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add user to request if token is valid
        request.user = get_user_from_token(request)
        response = self.get_response(request)
        return response