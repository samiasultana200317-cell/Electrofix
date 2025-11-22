import jwt
from django.conf import settings
from electrofix_app.mongodb import get_users_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


def get_user_from_token(request):
    """Return the user document (dict) for a valid Bearer token, otherwise None.

    This uses the PyMongo `users` collection so the rest of the codebase
    can operate against a single data layer.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            return None
        try:
            oid = ObjectId(user_id)
        except Exception:
            # If user_id is not a valid ObjectId, try as-is (some tokens might use string ids)
            oid = None

        users = get_users_collection()
        if oid:
            user = users.find_one({'_id': oid})
        else:
            user = users.find_one({'_id': user_id})

        return user
    except jwt.ExpiredSignatureError:
        logger.debug('JWT token expired')
        return None
    except jwt.InvalidTokenError:
        logger.debug('Invalid JWT token')
        return None


class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add user (document dict or None) to request if token is valid
        request.user = get_user_from_token(request)
        response = self.get_response(request)
        return response