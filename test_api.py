import os
import django
import json
import requests
from django.test import Client

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kogidi.settings')
django.setup()

# Create a test client
client = Client()

# Test student registration


def test_student_registration():
    print("\nTesting student registration...")
    data = {
        'email': 'new_student@example.com',
        'password': 'password123',
        'password2': 'password123',
        'first_name': 'New',
        'last_name': 'Student',
        'resident_state': 'Florida'
    }
    response = client.post('/api/auth/register/?type=student',
                           data=json.dumps(data), content_type='application/json')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")

# Test teacher registration


def test_teacher_registration():
    print("\nTesting teacher registration...")
    data = {
        'email': 'new_teacher@example.com',
        'password': 'password123',
        'password2': 'password123',
        'first_name': 'New',
        'last_name': 'Teacher',
        'resident_state': 'Ohio'
    }
    response = client.post('/api/auth/register/?type=teacher',
                           data=json.dumps(data), content_type='application/json')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")

# Test parent registration


def test_parent_registration():
    print("\nTesting parent registration...")
    data = {
        'email': 'new_parent@example.com',
        'password': 'password123',
        'password2': 'password123',
        'first_name': 'New',
        'last_name': 'Parent',
        'resident_state': 'Washington'
    }
    response = client.post('/api/auth/register/?type=parent',
                           data=json.dumps(data), content_type='application/json')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")

# Test student login


def test_student_login():
    print("\nTesting student login...")
    data = {
        'email': 'student@example.com',
        'password': 'password123'
    }
    response = client.post('/api/auth/login/?type=student',
                           data=json.dumps(data), content_type='application/json')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")

# Test teacher login


def test_teacher_login():
    print("\nTesting teacher login...")
    data = {
        'email': 'teacher@example.com',
        'password': 'password123'
    }
    response = client.post('/api/auth/login/?type=teacher',
                           data=json.dumps(data), content_type='application/json')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")

# Test parent login


def test_parent_login():
    print("\nTesting parent login...")
    data = {
        'email': 'parent@example.com',
        'password': 'password123'
    }
    response = client.post('/api/auth/login/?type=parent',
                           data=json.dumps(data), content_type='application/json')
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.content.decode()}")


# Run tests
if __name__ == '__main__':
    # First, create test users
    os.system('python create_test_users.py')

    # Test registration
    test_student_registration()
    test_teacher_registration()
    test_parent_registration()

    # Test login
    test_student_login()
    test_teacher_login()
    test_parent_login()
