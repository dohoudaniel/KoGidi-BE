import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kogidi.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if superuser exists
if not User.objects.filter(email='admin@kogidi.com').exists():
    User.objects.create_superuser(
        email='admin@kogidi.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        resident_state='New York'
    )
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
