from .helpers import validate_email, validate_phone

def validate_user_data(data):
    """Validate user registration data"""
    errors = {}
    
    if not data.get('name') or len(data['name'].strip()) < 2:
        errors['name'] = 'Name must be at least 2 characters long'
    
    if not data.get('email') or not validate_email(data['email']):
        errors['email'] = 'Please provide a valid email address'
    
    if not data.get('password') or len(data['password']) < 6:
        errors['password'] = 'Password must be at least 6 characters long'
    
    if not data.get('phone') or not validate_phone(data['phone']):
        errors['phone'] = 'Please provide a valid phone number'
    
    return errors

def validate_booking_data(data):
    """Validate booking data"""
    errors = {}
    
    required_fields = ['service', 'appliance_type', 'brand', 'model', 'problem_description', 'scheduled_date', 'time_slot']
    
    for field in required_fields:
        if not data.get(field):
            errors[field] = f'{field.replace("_", " ").title()} is required'
    
    if data.get('address'):
        required_address_fields = ['street', 'city', 'state', 'zipCode']
        for field in required_address_fields:
            if not data['address'].get(field):
                errors[f'address_{field}'] = f'Address {field} is required'
    
    return errors