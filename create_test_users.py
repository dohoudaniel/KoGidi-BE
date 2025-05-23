import os
import django
import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kogidi.settings')
django.setup()

from django.contrib.auth import get_user_model
from students.models import Student
from teachers.models import Teacher
from parents.models import Parent, ParentStudentRelationship

User = get_user_model()

# Create a student user
student_user, created = User.objects.get_or_create(
    email='student@example.com',
    defaults={
        'first_name': 'Student',
        'last_name': 'User',
        'resident_state': 'California',
        'is_student': True
    }
)

if created:
    student_user.set_password('password123')
    student_user.save()
    Student.objects.create(
        user=student_user,
        grade_level='10th Grade',
        date_of_birth=datetime.date(2006, 5, 15),
        school_name='California High School',
        interests='Math, Science, Programming'
    )
    print("Student user created successfully.")
else:
    print("Student user already exists.")

# Create a teacher user
teacher_user, created = User.objects.get_or_create(
    email='teacher@example.com',
    defaults={
        'first_name': 'Teacher',
        'last_name': 'User',
        'resident_state': 'New York',
        'is_teacher': True
    }
)

if created:
    teacher_user.set_password('password123')
    teacher_user.save()
    Teacher.objects.create(
        user=teacher_user,
        subject_specialization='Mathematics',
        years_of_experience=5,
        qualification='Master of Education',
        bio='Experienced math teacher with a passion for making learning fun.'
    )
    print("Teacher user created successfully.")
else:
    print("Teacher user already exists.")

# Create a parent user
parent_user, created = User.objects.get_or_create(
    email='parent@example.com',
    defaults={
        'first_name': 'Parent',
        'last_name': 'User',
        'resident_state': 'Texas',
        'is_parent': True
    }
)

if created:
    parent_user.set_password('password123')
    parent_user.save()
    parent = Parent.objects.create(
        user=parent_user,
        phone_number='555-123-4567',
        address='123 Main St, Austin, TX',
        occupation='Engineer'
    )
    
    # Create relationship with student
    student = Student.objects.first()
    if student:
        ParentStudentRelationship.objects.create(
            parent=parent,
            student=student,
            relationship='Father',
            is_primary=True
        )
    
    print("Parent user created successfully.")
else:
    print("Parent user already exists.")

# Create a superuser if it doesn't exist
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
