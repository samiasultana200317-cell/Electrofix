import json
import urllib.request

BASE='http://127.0.0.1:8000'

def do_register():
    payload = {
        'name': 'Test User',
        'email': 'testuser+ai@example.com',
        'password': 'TestPass123!',
        'phone': '+10000000000'
    }
    req = urllib.request.Request(BASE + '/api/auth/register/', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def do_login():
    payload = {'email': 'testuser+ai@example.com', 'password': 'TestPass123!'}
    req = urllib.request.Request(BASE + '/api/auth/login/', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def do_update(token):
    payload = {'name': 'Updated AI User', 'phone': '+19999999999'}
    req = urllib.request.Request(BASE + '/api/auth/profile/', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json', 'Authorization': f'Bearer {token}'}, method='PUT')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def do_get(token):
    req = urllib.request.Request(BASE + '/api/auth/profile/', headers={'Authorization': f'Bearer {token}'}, method='GET')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

if __name__ == '__main__':
    try:
        print('Attempting registration...')
        reg = do_register()
        print('REGISTER RESPONSE:', reg)
        token = reg.get('token')
    except Exception as e:
        print('Registration failed or user exists:', e)
        try:
            print('Trying login...')
            login = do_login()
            print('LOGIN RESPONSE:', login)
            token = login.get('token')
        except Exception as e2:
            print('Login failed:', e2)
            token = None

    if not token:
        print('No token, aborting')
    else:
        try:
            print('Updating profile...')
            upd = do_update(token)
            print('UPDATE RESPONSE:', upd)
        except Exception as e:
            print('Update failed:', e)
        try:
            print('Fetching profile...')
            prof = do_get(token)
            print('PROFILE:', prof)
        except Exception as e:
            print('Get profile failed:', e)
