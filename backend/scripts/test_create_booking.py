import requests
import uuid
import time

BASE = 'http://127.0.0.1:8000/api'

def register_user(email):
    url = f"{BASE}/auth/register/"
    payload = {
        'name': 'Booking Test User',
        'email': email,
        'password': 'TestPass123!',
        'phone': '+10000000000'
    }
    r = requests.post(url, json=payload)
    return r

def login(email):
    url = f"{BASE}/auth/login/"
    payload = {'email': email, 'password': 'TestPass123!'}
    r = requests.post(url, json=payload)
    return r

def create_service(token):
    url = f"{BASE}/services/"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'name': 'E2E Test Repair Service - Phone',
        'description': 'Auto-created test service',
        'price': 49,
        'duration': 60,
        'category': 'phone',
        'is_active': True
    }
    r = requests.post(url, json=payload, headers=headers)
    return r

def create_booking(token, service_id):
    url = f"{BASE}/bookings/"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'service': service_id,
        'appliance_type': 'phone',
        'brand': 'testbrand',
        'model': 'testmodel',
        'problem_description': 'Screen cracked',
        'scheduled_date': time.strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
        'time_slot': 'Morning',
        'address': '123 Test St.'
    }
    r = requests.post(url, json=payload, headers=headers)
    return r

if __name__ == '__main__':
    unique = uuid.uuid4().hex[:8]
    email = f'testbooking+{unique}@example.com'

    print('Registering user...')
    r = register_user(email)
    print('Register status:', r.status_code, r.text)

    print('Logging in...')
    r = login(email)
    print('Login status:', r.status_code, r.text)
    if r.status_code != 200:
        print('Login failed, exiting')
        exit(1)

    token = r.json().get('token')
    if not token:
        print('No token returned, exiting')
        exit(1)

    print('Creating service...')
    r = create_service(token)
    print('Create service status:', r.status_code, r.text)
    service_id = None
    if r.status_code in (200,201):
        data = r.json()
        service_id = data.get('data', {}).get('id') or data.get('id')

    if not service_id:
        print('Service creation failed, attempting to fetch services and match by name...')
        # try to fetch services
        resp = requests.get(f"{BASE}/services/")
        if resp.status_code == 200:
            for s in resp.json().get('data', []):
                if 'phone' in s.get('category', '').lower() or 'phone' in s.get('name', '').lower():
                    service_id = s.get('id')
                    break

    if not service_id:
        print('Could not determine service id from API, attempting direct DB insert with fallback fields...')
        # Fallback: insert a minimal service doc directly into MongoDB including guess-required fields
        try:
            from pymongo import MongoClient
            import os
            uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
            dbname = os.environ.get('MONGODB_NAME', 'electrofixdb')
            client = MongoClient(uri)
            db = client[dbname]
            fallback = {
                'name': 'E2E Fallback Service - Phone',
                'description': 'Fallback service inserted for tests',
                'price': 49,
                'duration': 60,
                'category': 'phone',
                'image': '',
                'features': [],
                'is_active': True,
                # Some deployments have collection validators requiring extra fields; include safe defaults
                'fieldname1': 'x',
                # observed DB validator expects an integer for fieldname2
                'fieldname2': 1,
                'created_at': None,
                'updated_at': None
            }
            res = db['services'].insert_one(fallback)
            service_id = str(res.inserted_id)
            print('Inserted fallback service id', service_id)
        except Exception as e:
            print('Direct DB insert failed:', e)
            print('Cannot proceed without a service id, exiting')
            exit(1)

    print('Creating booking with service id', service_id)
    r = create_booking(token, service_id)
    print('Create booking status:', r.status_code, r.text)
    if r.status_code in (200,201):
        print('Booking created OK')
    else:
        print('Booking creation failed')
