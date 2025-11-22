from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from electrofix_app.mongodb import get_services_collection
from utils.serializers import serialize_doc, serialize_list
from bson import ObjectId
from utils.auth import get_user_from_token


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_services(request):
    try:
        services_collection = get_services_collection()

        if request.method == 'GET':
            services = list(services_collection.find({'is_active': True}))
            services_data = serialize_list(services)
            return Response({'success': True, 'data': services_data})

        # POST -> create service (requires auth)
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        # Basic required fields validation
        required = ['name', 'description', 'price']
        for f in required:
            if not data.get(f):
                return Response({'success': False, 'message': f'{f} is required'}, status=status.HTTP_400_BAD_REQUEST)

        doc = {
            'name': data.get('name'),
            'description': data.get('description'),
            'price': data.get('price'),
            'duration': data.get('duration'),
            'category': data.get('category'),
            'image': data.get('image'),
            'features': data.get('features', []),
            'is_active': data.get('is_active', True),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = services_collection.insert_one(doc)
        doc['id'] = str(result.inserted_id)
        doc.pop('_id', None)

        return Response({'success': True, 'message': 'Service created successfully', 'data': doc}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_service(request, service_id):
    try:
        services_collection = get_services_collection()
        try:
            oid = ObjectId(service_id)
        except Exception:
            oid = service_id

        service = services_collection.find_one({'_id': oid})
        if not service:
            return Response({'success': False, 'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'success': True, 'data': serialize_doc(service)})

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_service(request):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        services_collection = get_services_collection()

        # Basic required fields validation
        required = ['name', 'description', 'price']
        for f in required:
            if not data.get(f):
                return Response({'success': False, 'message': f'{f} is required'}, status=status.HTTP_400_BAD_REQUEST)

        doc = {
            'name': data.get('name'),
            'description': data.get('description'),
            'price': data.get('price'),
            'duration': data.get('duration'),
            'category': data.get('category'),
            'image': data.get('image'),
            'features': data.get('features', []),
            'is_active': data.get('is_active', True),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = services_collection.insert_one(doc)
        doc['id'] = str(result.inserted_id)
        doc.pop('_id', None)

        return Response({'success': True, 'message': 'Service created successfully', 'data': serialize_doc(doc)}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)