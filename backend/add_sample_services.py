import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrofix_project.settings')
django.setup()

from electrofix_app.mongodb import get_services_collection

services_collection = get_services_collection()

# Clear existing services
services_collection.delete_many({})

# Add sample services
sample_services = [
    {
        'name': 'Basic Appliance Repair',
        'description': 'Professional diagnosis and repair of common appliance issues',
        'price': 79.99,
        'duration': '1-2 hours',
        'category': 'repair',
        'features': ['Comprehensive diagnosis', 'Parts replacement', '30-day service warranty'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Annual Maintenance Service',
        'description': 'Preventive maintenance to keep your appliances running efficiently',
        'price': 59.99,
        'duration': '1 hour',
        'category': 'maintenance',
        'features': ['Complete inspection', 'Cleaning and lubrication', 'Performance optimization'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'New Appliance Installation',
        'description': 'Professional installation of new appliances',
        'price': 99.99,
        'duration': '2-3 hours',
        'category': 'installation',
        'features': ['Professional installation', 'Safety testing', 'Operation demonstration'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Emergency Repair Service',
        'description': '24/7 emergency repair for urgent appliance issues',
        'price': 129.99,
        'duration': '2-3 hours',
        'category': 'repair',
        'features': ['24/7 availability', 'Rapid response', 'Emergency parts'],
        'is_active': True,
        'created_at': datetime.utcnow()
    }
]

result = services_collection.insert_many(sample_services)
print(f'✅ Added {len(result.inserted_ids)} sample services')
