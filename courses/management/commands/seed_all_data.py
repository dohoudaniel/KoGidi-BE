from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date
import random

from courses.models import Course, StudentProgress, Assignment, Achievement, StudentStats
from students.models import Student
from teachers.models import Teacher, TeacherClass, TeacherStats
from parents.models import Parent

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data for existing users'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Starting database seeding (using existing users)...\n')
        
        # Get existing users
        students = User.objects.filter(student_profile__isnull=False)
        teachers = User.objects.filter(teacher_profile__isnull=False)
        parents = User.objects.filter(parent_profile__isnull=False)
        
        if not students.exists():
            self.stdout.write(self.style.WARNING('⚠️  No students found. Please create student users first.'))
            return
        
        # Seed in order
        courses = self.create_courses()
        self.create_student_data(list(students), courses)
        
        if teachers.exists():
            self.create_teacher_data(list(teachers), courses)
        else:
            self.stdout.write(self.style.WARNING('⚠️  No teachers found. Skipping teacher data.'))
        
        if parents.exists() and students.exists():
            self.create_parent_data(list(parents), list(students))
        else:
            self.stdout.write(self.style.WARNING('⚠️  No parents found. Skipping parent links.'))
        
        self.create_assignments(courses, list(students))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'''
📊 Summary:
   - Students: {students.count()}
   - Teachers: {teachers.count()}
   - Parents: {parents.count()}
   - Courses: {len(courses)}
   - Data created for all existing users
        '''))

    def create_courses(self):
        """Create sample courses if they don't exist"""
        self.stdout.write('📚 Ensuring courses exist...')
        
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
        
        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            courses.append(course)
            if created:
                self.stdout.write(f'  ✅ Created course: {course.title}')
            else:
                self.stdout.write(f'  ℹ️  Course exists: {course.title}')
        
        return courses

    def create_student_data(self, students, courses):
        """Create student progress, stats, and achievements for existing students"""
        self.stdout.write('📈 Creating student progress data...')
        
        for student in students:
            # Enroll student in 2-4 random courses
            num_courses = min(random.randint(2, 4), len(courses))
            enrolled_courses = random.sample(courses, num_courses)
            
            for course in enrolled_courses:
                progress, created = StudentProgress.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'progress_percentage': random.randint(10, 95),
                        'completed_lessons': random.randint(1, max(1, course.total_lessons - 2)),
                        'time_spent_minutes': random.randint(60, 500),
                        'average_score': random.uniform(60, 95),
                        'is_completed': False,
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Progress: {student.email} → {course.title}')
            
            # Create/update student stats
            total_progress = StudentProgress.objects.filter(student=student)
            if total_progress.exists():
                stats, created = StudentStats.objects.update_or_create(
                    student=student,
                    defaults={
                        'total_courses': total_progress.count(),
                        'completed_courses': total_progress.filter(is_completed=True).count(),
                        'current_streak': random.randint(1, 14),
                        'total_hours': sum(p.time_spent_minutes for p in total_progress) // 60,
                        'average_score': sum(p.average_score for p in total_progress) / total_progress.count(),
                    }
                )
            
            # Create achievements
            achievement_types = [
                ('First Course Enrolled', 'course_completion', '🎯'),
                ('7-Day Streak', 'streak', '🔥'),
                ('High Achiever', 'score', '⭐'),
                ('Fast Learner', 'milestone', '🚀'),
            ]
            
            for title, ach_type, icon in random.sample(achievement_types, random.randint(1, 3)):
                Achievement.objects.get_or_create(
                    student=student,
                    title=title,
                    defaults={
                        'achievement_type': ach_type,
                        'icon': icon,
                        'description': f'Earned for {title.lower()}',
                    }
                )

    def create_teacher_data(self, teachers, courses):
        """Create teacher classes and stats for existing teachers"""
        self.stdout.write('👨‍🏫 Creating teacher data...')
        
        for teacher in teachers:
            # Create 2-3 classes for this teacher
            num_classes = min(random.randint(2, 3), len(courses))
            selected_courses = random.sample(courses, num_classes)
            
            for course in selected_courses:
                class_obj, created = TeacherClass.objects.get_or_create(
                    teacher=teacher,
                    course=course,
                    defaults={
                        'name': f'{course.title} - {course.grade.upper().replace("_", " ")}',
                        'description': f'A class for {course.grade.upper().replace("_", " ")} students',
                        'total_students': random.randint(10, 25),
                        'progress_percentage': random.randint(30, 85),
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Class: {class_obj.name}')
            
            # Create/update teacher stats
            classes = TeacherClass.objects.filter(teacher=teacher)
            if classes.exists():
                TeacherStats.objects.update_or_create(
                    teacher=teacher,
                    defaults={
                        'total_students': sum(c.total_students for c in classes),
                        'active_courses': classes.count(),
                        'pending_assignments': random.randint(5, 20),
                        'average_class_score': random.uniform(70, 85),
                    }
                )

    def create_parent_data(self, parents, students):
        """Link existing parents to existing students"""
        self.stdout.write('👨‍👩‍👧 Linking parents to students...')
        
        from parents.models import ParentStudentRelationship
        
        for parent in parents:
            parent_profile = parent.parent_profile
            # Link to 1-2 random students
            num_children = min(random.randint(1, 2), len(students))
            children = random.sample(students, num_children)
            
            for student in children:
                relationship, created = ParentStudentRelationship.objects.get_or_create(
                    parent=parent_profile,
                    student=student.student_profile,
                    defaults={
                        'relationship': random.choice(['Father', 'Mother', 'Guardian']),
                        'is_primary': True,
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Linked: {parent.email} → {student.email}')

    def create_assignments(self, courses, students):
        """Create assignments for courses"""
        self.stdout.write('📝 Creating assignments...')
        
        if not students:
            self.stdout.write('  ⚠️  No students found, skipping assignments')
            return
        
        assignment_templates = [
            ('Quiz', 'high', 'Complete the chapter quiz'),
            ('Essay', 'medium', 'Write a comprehensive essay'),
            ('Project', 'high', 'Complete the group project'),
            ('Homework', 'low', 'Complete homework exercises'),
            ('Presentation', 'medium', 'Prepare and deliver a presentation'),
        ]
        
        total_created = 0
        for course in courses:
            # Create 2-4 assignments per course
            for i in range(random.randint(2, 4)):
                title_prefix, priority, description = random.choice(assignment_templates)
                
                # Assign to random students
                num_students = min(random.randint(3, 7), len(students))
                assigned_students = random.sample(students, num_students)
                
                for student in assigned_students:
                    due_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
                    
                    assignment, created = Assignment.objects.get_or_create(
                        course=course,
                        student=student,
                        title=f'{course.subject} {title_prefix} {i+1}',
                        defaults={
                            'description': f'{description} for {course.title}',
                            'priority': priority,
                            'status': random.choice(['pending', 'submitted', 'submitted', 'graded']),
                            'due_date': due_date,
                            'score': random.uniform(60, 100) if random.choice([True, False]) else None,
                        }
                    )
                    if created:
                        total_created += 1
        
        self.stdout.write(f'  ✅ Created {total_created} assignments')
