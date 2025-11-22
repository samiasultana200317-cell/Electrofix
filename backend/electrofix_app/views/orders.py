from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from electrofix_app.mongodb import get_orders_collection, get_users_collection, get_technicians_collection, get_services_collection
from utils.serializers import serialize_doc, serialize_list
from utils.auth import get_user_from_token
from datetime import datetime
from bson import ObjectId


@api_view(['POST'])
def create_order(request):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        items = data.get('items') or []
        preferred_technician = data.get('preferred_technician')

        if not items:
            return Response({'success': False, 'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        services_collection = get_services_collection()
        # Normalize items and compute total
        total = 0
        normalized_items = []
        for it in items:
            # support multiple naming conventions from frontend
            pid = it.get('productId') or it.get('serviceId') or it.get('id') or it.get('service_id') or it.get('product_id')
            qty = 1
            try:
                qty = int(it.get('quantity', 1))
            except Exception:
                qty = 1

            svc = None
            # try ObjectId lookup first (if pid looks like ObjectId)
            if pid:
                try:
                    svc_oid = ObjectId(pid)
                    svc = services_collection.find_one({'_id': svc_oid})
                except Exception:
                    # fallback: try looking up by string id fields
                    try:
                        svc = services_collection.find_one({'id': str(pid)}) or services_collection.find_one({'_id': str(pid)})
                    except Exception:
                        svc = None

            # determine price safely
            price = 0
            if svc and isinstance(svc.get('price', None), (int, float)):
                price = svc.get('price')
            else:
                try:
                    price = float(it.get('price', 0) or 0)
                except Exception:
                    price = 0

            total += price * qty
            normalized_items.append({
                'productId': str(pid) if pid is not None else None,
                'title': it.get('title') or (svc.get('name') if svc else ''),
                'price': price,
                'quantity': qty
            })

        orders_collection = get_orders_collection()

        order = {
            'user_id': user.get('_id'),
            'items': normalized_items,
            'total': total,
            'preferred_technician': preferred_technician,
            'status': 'pending',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        result = orders_collection.insert_one(order)

        # Prepare a JSON-serializable response using helper
        order['id'] = str(result.inserted_id)
        order_out = serialize_doc(order)
        return Response({'success': True, 'message': 'Order created', 'data': order_out}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_orders(request):
    try:
        user = get_user_from_token(request)
        if not user:
            return Response({'success': False, 'message': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        orders_collection = get_orders_collection()
        docs = list(orders_collection.find({'user_id': user.get('_id')}).sort('created_at', -1))

        results = serialize_list(docs)

        return Response({'success': True, 'data': results})

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_technicians(request):
    try:
        techs = list(get_technicians_collection().find({}))
        out = []
        for t in techs:
            t['id'] = str(t.get('_id'))
            t.pop('_id', None)
            out.append(t)
        return Response({'success': True, 'data': out})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
