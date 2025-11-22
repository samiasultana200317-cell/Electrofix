#!/usr/bin/env python
"""Seed the `technicians` collection with sample documents for local development.

Run from the repo root (or backend folder):
  python backend/scripts/seed_technicians.py
"""
import os
import sys
from datetime import datetime

# Ensure Django settings are available
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrofix_project.settings')
try:
    import django
    django.setup()
except Exception as e:
    print('Failed to setup Django:', e)
    sys.exit(1)

from electrofix_app.mongodb import get_technicians_collection


def seed():
    col = get_technicians_collection()

    samples = [
        {
            'name': 'Alex Morgan',
            'phone': '+15550101001',
            'email': 'alex.morgan@example.com',
            'skills': ['phone', 'tablet', 'screen'],
            'location': 'Downtown',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'name': 'Priya Singh',
            'phone': '+15550101002',
            'email': 'priya.singh@example.com',
            'skills': ['laptop', 'battery', 'diagnostics'],
            'location': 'Uptown',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'name': 'Miguel Alvarez',
            'phone': '+15550101003',
            'email': 'miguel.alvarez@example.com',
            'skills': ['water damage', 'board level repair'],
            'location': 'Midtown',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
    ]

    try:
        res = col.insert_many(samples)
        print('Inserted technicians:', [str(x) for x in res.inserted_ids])
    except Exception as e:
        print('Error inserting technicians:', e)


if __name__ == '__main__':
    seed()
