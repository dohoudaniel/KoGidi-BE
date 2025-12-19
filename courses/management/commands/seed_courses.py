from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from courses.models import Course, Assignment


class Command(BaseCommand):
    help = 'Seed database with sample courses and assignments'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database with sample data...')
        
        # Create sample courses
        courses_data = [
            {
                'title': 'Introduction to Mathematics',
                'description': 'Learn basic mathematical concepts including arithmetic, algebra, and geometry',
                'subject': 'Mathematics',
                'grade': 'primary_4',
                'level': 'beginner',
                'duration': '4 weeks',
                'category': 'Mathematics',
                'total_lessons': 12,
            },
            {
                'title': 'Basic Science',
                'description': 'Explore fundamental science principles including physics, chemistry, and biology',
                'subject': 'Science',
                'grade': 'primary_5',
                'level': 'beginner',
                'duration': '6 weeks',
                'category': 'Science',
                'total_lessons': 18,
            },
            {
                'title': 'Yoruba Language',
                'description': 'Learn Yoruba language basics including grammar, vocabulary, and cultural context',
                'subject': 'Language',
                'grade': 'primary_3',
                'level': 'beginner',
                'duration': '8 weeks',
                'category': 'Language',
                'language': 'Yoruba',
                'total_lessons': 24,
            },
            {
                'title': 'English Language',
                'description': 'Improve your English skills with grammar, reading comprehension, and writing',
                'subject': 'English',
                'grade': 'jss_1',
                'level': 'intermediate',
                'duration': '10 weeks',
                'category': 'Language',
                'total_lessons': 30,
            },
            {
                'title': 'Computer Studies',
                'description': 'Introduction to computers, programming basics, and digital literacy',
                'subject': 'Computer Science',
                'grade': 'jss_2',
                'level': 'beginner',
                'duration': '8 weeks',
                'category': 'Technology',
                'total_lessons': 20,
            },
            {
                'title': 'Social Studies',
                'description': 'Learn about Nigerian history, geography, and civic education',
                'subject': 'Social Studies',
                'grade': 'primary_6',
                'level': 'intermediate',
                'duration': '6 weeks',
                'category': 'Social Sciences',
                'total_lessons': 15,
            },
            {
                'title': 'Basic Technology',
                'description': 'Introduction to technical drawing, woodwork, and basic engineering concepts',
                'subject': 'Technology',
                'grade': 'jss_1',
                'level': 'beginner',
                'duration': '8 weeks',
                'category': 'Technology',
                'total_lessons': 16,
            },
            {
                'title': 'Agricultural Science',
                'description': 'Learn about farming, animal husbandry, and soil science',
                'subject': 'Agriculture',
                'grade': 'jss_3',
                'level': 'intermediate',
                'duration': '10 weeks',
                'category': 'Science',
                'total_lessons': 22,
            },
        ]
        
        created_courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
                created_courses.append(course)
            else:
                self.stdout.write(f'Course already exists: {course.title}')
        
        # Create sample general assignments (not tied to specific students)
        if created_courses:
            assignments_data = [
                {
                    'course': created_courses[0],
                    'title': 'Mathematics Quiz',
                    'description': 'Complete the introductory mathematics problems',
                    'priority': 'high',
                    'due_date': timezone.now().date() + timedelta(days=5),
                },
                {
                    'course': created_courses[1],
                    'title': 'Science Project',
                    'description': 'Create a simple science experiment and report your findings',
                    'priority': 'medium',
                    'due_date': timezone.now().date() + timedelta(days=10),
                },
                {
                    'course': created_courses[3],
                    'title': 'English Essay',
                    'description': 'Write a 500-word essay on a topic of your choice',
                    'priority': 'medium',
                    'due_date': timezone.now().date() + timedelta(days=8),
                },
            ]
            
            for assignment_data in assignments_data:
                assignment, created = Assignment.objects.get_or_create(
                    title=assignment_data['title'],
                    course=assignment_data['course'],
                    defaults=assignment_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created assignment: {assignment.title}'))
                else:
                    self.stdout.write(f'Assignment already exists: {assignment.title}')
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
