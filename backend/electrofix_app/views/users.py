from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from electrofix_app.mongodb import get_users_collection
from utils.serializers import serialize_doc, serialize_list
from utils.auth import get_user_from_token
from bson import ObjectId


@api_view(['PUT'])
def update_profile(request):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        users_collection = get_users_collection()

        update_fields = {}
        if 'name' in data:
            update_fields['name'] = data['name']
        if 'phone' in data:
            update_fields['phone'] = data['phone']
        if 'address' in data:
            update_fields['address'] = data['address']

        if update_fields:
            users_collection.update_one({'_id': user.get('_id')}, {'$set': update_fields})

        # Return fresh document
        updated = users_collection.find_one({'_id': user.get('_id')})
        if updated:
            user_out = serialize_doc(updated, exclude_fields=['password'])
        else:
            user_out = None

        return Response({'success': True, 'message': 'Profile updated successfully', 'user': user_out})

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_users(request):
    try:
        users_collection = get_users_collection()
        docs = list(users_collection.find())
        users_data = serialize_list(docs, exclude_fields=['password'])

        return Response({'success': True, 'data': users_data})

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)