from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from electrofix_app.mongodb import get_bookings_collection, get_services_collection, get_users_collection, get_technicians_collection
from utils.serializers import serialize_doc, serialize_list
from utils.auth import get_user_from_token
from datetime import datetime
from bson import ObjectId


@api_view(['POST'])
def create_booking(request):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        # Validate required fields (service is optional for freeform repair requests)
        required_fields = ['appliance_type', 'brand', 'model', 'problem_description', 'scheduled_date', 'time_slot', 'address']
        for field in required_fields:
            if not data.get(field):
                return Response({'success': False, 'message': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        services_collection = get_services_collection()
        bookings_collection = get_bookings_collection()

        # Resolve service (optional). If a service id is provided, try to find it; otherwise allow freeform request.
        service = None
        service_id_val = data.get('service')
        if service_id_val:
            try:
                svc_id = ObjectId(service_id_val)
            except Exception:
                svc_id = service_id_val
            service = services_collection.find_one({'_id': svc_id})

        # Create booking document
        booking_data = {
            'user_id': user.get('_id'),
            'service_id': service.get('_id') if service else None,
            # preferred_technician may be provided by frontend (id string)
            'preferred_technician': None,
            'appliance_type': data.get('appliance_type'),
            'brand': data.get('brand'),
            'model': data.get('model'),
            'problem_description': data.get('problem_description'),
            'address': data.get('address'),
            'scheduled_date': datetime.fromisoformat(data.get('scheduled_date').replace('Z', '+00:00')),
            'time_slot': data.get('time_slot'),
            'status': 'pending',
            'total_cost': service.get('price', 0) if service else 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        # Accept preferred_technician from payload (optional)
        pref = data.get('preferred_technician')
        if pref:
            try:
                booking_data['preferred_technician'] = ObjectId(pref)
            except Exception:
                booking_data['preferred_technician'] = pref

        result = bookings_collection.insert_one(booking_data)

        # Prepare a JSON-serializable response: remove internal ObjectId and convert dates/ids to strings
        booking_data['id'] = str(result.inserted_id)
        return Response({'success': True, 'message': 'Booking created successfully', 'data': serialize_doc(booking_data)}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_bookings(request):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        bookings_collection = get_bookings_collection()
        services_collection = get_services_collection()
        technicians_collection = get_technicians_collection()

        user_id = user.get('_id')

        # Aggregation pipeline: match bookings for user, lookup service and technician documents
        pipeline = [
            { '$match': { 'user_id': user_id } },
            { '$sort': { 'created_at': -1 } },
            { '$lookup': {
                'from': 'services',
                'localField': 'service_id',
                'foreignField': '_id',
                'as': 'service'
            }},
            { '$unwind': { 'path': '$service', 'preserveNullAndEmptyArrays': True } },
            { '$lookup': {
                'from': 'technicians',
                'localField': 'technician_id',
                'foreignField': '_id',
                'as': 'technician'
            }},
            { '$unwind': { 'path': '$technician', 'preserveNullAndEmptyArrays': True } },
            { '$project': {
                '_id': 1,
                'user_id': 1,
                'service_id': 1,
                'technician_id': 1,
                'preferred_technician': 1,
                'appliance_type': 1,
                'brand': 1,
                'model': 1,
                'problem_description': 1,
                'address': 1,
                'scheduled_date': 1,
                'time_slot': 1,
                'status': 1,
                'total_cost': 1,
                'created_at': 1,
                'updated_at': 1,
                'service': {
                    'id': '$service._id',
                    'name': '$service.name',
                    'price': '$service.price',
                    'duration_minutes': '$service.duration_minutes'
                },
                'technician': {
                    'id': '$technician._id',
                    'name': '$technician.name',
                    'phone': '$technician.phone',
                    'email': '$technician.email'
                }
            }}
        ]

        docs = list(bookings_collection.aggregate(pipeline))

        # Format results: convert ObjectIds to strings and datetimes to isoformat
        def fmt(d):
            out = {
                'id': str(d.get('_id')),
                'user_id': str(d.get('user_id')) if d.get('user_id') else None,
                'service_id': str(d.get('service_id')) if d.get('service_id') else None,
                'technician_id': str(d.get('technician_id')) if d.get('technician_id') else None,
                'preferred_technician': str(d.get('preferred_technician')) if d.get('preferred_technician') else None,
                'appliance_type': d.get('appliance_type'),
                'brand': d.get('brand'),
                'model': d.get('model'),
                'problem_description': d.get('problem_description'),
                'address': d.get('address'),
                'scheduled_date': d.get('scheduled_date').isoformat() if d.get('scheduled_date') else None,
                'time_slot': d.get('time_slot'),
                'status': d.get('status'),
                'total_cost': d.get('total_cost'),
                'created_at': d.get('created_at').isoformat() if d.get('created_at') else None,
                'updated_at': d.get('updated_at').isoformat() if d.get('updated_at') else None,
                'service': None,
                'technician': None
            }

            svc = d.get('service')
            if svc:
                out['service'] = {
                    'id': str(svc.get('id')) if svc.get('id') else None,
                    'name': svc.get('name'),
                    'price': svc.get('price'),
                    'duration_minutes': svc.get('duration_minutes')
                }

            tech = d.get('technician')
            if tech:
                out['technician'] = {
                    'id': str(tech.get('id')) if tech.get('id') else None,
                    'name': tech.get('name'),
                    'phone': tech.get('phone'),
                    'email': tech.get('email')
                }

            return out

        results = [fmt(d) for d in docs]

        return Response({'success': True, 'data': results})

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_booking(request, booking_id):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        bookings_collection = get_bookings_collection()
        try:
            bid = ObjectId(booking_id)
        except Exception:
            bid = booking_id

        booking = bookings_collection.find_one({'_id': bid, 'user_id': user.get('_id')})
        if not booking:
            return Response({'success': False, 'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        booking['id'] = str(booking.get('_id'))
        booking.pop('_id', None)
        return Response({'success': True, 'data': booking})

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)