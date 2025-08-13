#!/usr/bin/env python
"""
Simple startup script to test the Django application
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# Import Django
import django
django.setup()

# Test basic Django functionality
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Django application is ready!")
    print(f"Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"Current directory: {os.getcwd()}")
    
    # Test running a simple Django command
    try:
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Django check passed!")
    except Exception as e:
        print(f"❌ Django check failed: {e}")
        sys.exit(1)
