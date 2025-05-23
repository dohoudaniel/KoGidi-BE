import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kogidi.settings')
django.setup()

from django.contrib.auth import get_user_model
from students.models import Student
from teachers.models import Teacher
from parents.models import Parent, ParentStudentRelationship

User = get_user_model()

# Check if our models are properly set up
print("\nVerifying User model...")
print(f"User model: {User.__name__}")
print(f"User fields: {[field.name for field in User._meta.fields]}")

print("\nVerifying Student model...")
print(f"Student model: {Student.__name__}")
print(f"Student fields: {[field.name for field in Student._meta.fields]}")

print("\nVerifying Teacher model...")
print(f"Teacher model: {Teacher.__name__}")
print(f"Teacher fields: {[field.name for field in Teacher._meta.fields]}")

print("\nVerifying Parent model...")
print(f"Parent model: {Parent.__name__}")
print(f"Parent fields: {[field.name for field in Parent._meta.fields]}")

print("\nVerifying ParentStudentRelationship model...")
print(f"ParentStudentRelationship model: {ParentStudentRelationship.__name__}")
print(f"ParentStudentRelationship fields: {[field.name for field in ParentStudentRelationship._meta.fields]}")

# Create test users if they don't exist
if not User.objects.filter(email='student@example.com').exists():
    print("\nCreating test student user...")
    student_user = User.objects.create_user(
        email='student@example.com',
        password='password123',
        first_name='Student',
        last_name='User',
        resident_state='California',
        is_student=True
    )
    Student.objects.create(
        user=student_user,
        grade_level='10th Grade',
        school_name='California High School'
    )
    print("Student user created successfully.")

if not User.objects.filter(email='teacher@example.com').exists():
    print("\nCreating test teacher user...")
    teacher_user = User.objects.create_user(
        email='teacher@example.com',
        password='password123',
        first_name='Teacher',
        last_name='User',
        resident_state='New York',
        is_teacher=True
    )
    Teacher.objects.create(
        user=teacher_user,
        subject_specialization='Mathematics',
        years_of_experience=5,
        qualification='Master of Education'
    )
    print("Teacher user created successfully.")

if not User.objects.filter(email='parent@example.com').exists():
    print("\nCreating test parent user...")
    parent_user = User.objects.create_user(
        email='parent@example.com',
        password='password123',
        first_name='Parent',
        last_name='User',
        resident_state='Texas',
        is_parent=True
    )
    Parent.objects.create(
        user=parent_user,
        phone_number='555-123-4567',
        address='123 Main St, Austin, TX'
    )
    print("Parent user created successfully.")

# List all users
print("\nListing all users...")
for user in User.objects.all():
    print(f"User: {user.email}, Name: {user.get_full_name()}, Student: {user.is_student}, Teacher: {user.is_teacher}, Parent: {user.is_parent}")

# List all students
print("\nListing all students...")
for student in Student.objects.all():
    print(f"Student: {student.user.email}, Name: {student.user.get_full_name()}, Grade: {student.grade_level}, School: {student.school_name}")

# List all teachers
print("\nListing all teachers...")
for teacher in Teacher.objects.all():
    print(f"Teacher: {teacher.user.email}, Name: {teacher.user.get_full_name()}, Subject: {teacher.subject_specialization}, Experience: {teacher.years_of_experience} years")

# List all parents
print("\nListing all parents...")
for parent in Parent.objects.all():
    print(f"Parent: {parent.user.email}, Name: {parent.user.get_full_name()}, Phone: {parent.phone_number}")

print("\nVerification complete!")
