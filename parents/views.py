from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Parent, ParentStudentRelationship
from .serializers import ParentSerializer, ParentProfileUpdateSerializer, ParentStudentRelationshipSerializer
from courses.models import StudentProgress, Assignment, Achievement
from courses.serializers import StudentProgressSerializer, AssignmentSerializer, AchievementSerializer


class IsParentUser(IsAuthenticated):
    """
    Custom permission to only allow parents to access their own profile

    This permission class checks if:
    1. The user is authenticated
    2. The user has a parent profile
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, 'parent_profile')


class ParentProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving parent profile

    This endpoint allows authenticated parent users to retrieve their profile information.

    Returns:
    - 200 OK: Parent profile data
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a parent
    """
    serializer_class = ParentSerializer
    permission_classes = [IsParentUser]

    @swagger_auto_schema(
        responses={
            200: ParentSerializer,
            401: "User is not authenticated",
            403: "User is not a parent"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.parent_profile


class ParentProfileUpdateView(generics.UpdateAPIView):
    """
    API view for updating parent profile

    This endpoint allows authenticated parent users to update their profile information.

    Request Body:
    - phone_number: Parent's phone number (optional)
    - address: Parent's address (optional)
    - occupation: Parent's occupation (optional)
    - first_name: Parent's first name (optional)
    - last_name: Parent's last name (optional)
    - resident_state: Parent's resident state (optional)

    Returns:
    - 200 OK: Parent profile updated successfully
    - 400 Bad Request: Invalid data provided
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a parent
    """
    serializer_class = ParentProfileUpdateSerializer
    permission_classes = [IsParentUser]

    def get_object(self):
        return self.request.user.parent_profile

    @swagger_auto_schema(
        request_body=ParentProfileUpdateSerializer,
        responses={
            200: ParentSerializer,
            400: "Invalid data provided",
            401: "User is not authenticated",
            403: "User is not a parent"
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(ParentSerializer(instance).data)


class ParentDashboardView(APIView):
    """
    Combined API view for parent dashboard data
    Returns information about all children and their progress
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all dashboard data for authenticated parent",
        responses={
            200: "Dashboard data",
            401: "Unauthorized",
            403: "Not a parent"
        }
    )
    def get(self, request):
        """
        Get comprehensive parent dashboard data
        """
        user = request.user

        # Check if user is a parent
        if not hasattr(user, 'parent_profile'):
            return Response(
                {'error': 'Only parents can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )

        parent_profile = user.parent_profile

        # Get all children relationships
        relationships = ParentStudentRelationship.objects.filter(
            parent=parent_profile
        ).select_related('student', 'student__user')

        if not relationships.exists():
            return Response({
                'children': [],
                'total_children': 0,
                'stats': {
                    'total_courses': 0,
                    'total_assignments': 0,
                    'completed_courses': 0,
                    'upcoming_assignments': 0,
                },
                'message': 'No children linked to this account'
            })

        # Collect data for all children
        children_data = []
        total_courses = 0
        total_assignments = 0
        completed_courses = 0
        upcoming_assignments = 0

        for rel in relationships:
            student = rel.student
            student_user = student.user

            # Get student progress
            progress_records = StudentProgress.objects.filter(student=student_user).select_related('course')
            
            # Get assignments
            assignments = Assignment.objects.filter(student=student_user).select_related('course')
            pending_assignments = assignments.filter(status='pending')
            
            # Get achievements
            achievements = Achievement.objects.filter(student=student_user)

            # Calculate stats for this child
            child_total_courses = progress_records.count()
            child_completed = progress_records.filter(is_completed=True).count()
            child_avg_score = sum(p.average_score for p in progress_records) / child_total_courses if child_total_courses > 0 else 0
            child_total_hours = sum(p.time_spent_minutes for p in progress_records) // 60

            # Aggregate
            total_courses += child_total_courses
            total_assignments += assignments.count()
            completed_courses += child_completed
            upcoming_assignments += pending_assignments.count()

            # Serialize progress and assignments
            progress_data = [{
                'course_id': p.course.id,
                'course_title': p.course.title,
                'progress_percentage': p.progress_percentage,
                'completed_lessons': p.completed_lessons,
                'total_lessons': p.course.total_lessons,
                'average_score': p.average_score,
                'is_completed': p.is_completed,
            } for p in progress_records[:5]]  # Limit to 5 recent

            recent_assignments = [{
                'id': a.id,
                'title': a.title,
                'course_title': a.course.title if a.course else 'N/A',
                'due_date': a.due_date.strftime('%Y-%m-%d') if a.due_date else None,
                'status': a.status,
                'priority': a.priority,
                'score': a.score,
            } for a in assignments.order_by('due_date')[:5]]  # Limit to 5 upcoming

            achievements_data = [{
                'id': ach.id,
                'title': ach.title,
                'icon': ach.icon,
                'earned_at': ach.earned_at.strftime('%Y-%m-%d') if ach.earned_at else None,
            } for ach in achievements[:5]]

            child_data = {
                'id': student.id,
                'name': student_user.get_full_name(),
                'email': student_user.email,
                'grade_level': student.grade_level,
                'school_name': student.school_name,
                'relationship': rel.relationship,
                'is_primary': rel.is_primary,
                'stats': {
                    'total_courses': child_total_courses,
                    'completed_courses': child_completed,
                    'average_score': round(child_avg_score, 2),
                    'total_hours': child_total_hours,
                    'total_assignments': assignments.count(),
                    'pending_assignments': pending_assignments.count(),
                },
                'progress': progress_data,
                'recent_assignments': recent_assignments,
                'achievements': achievements_data,
            }
            children_data.append(child_data)

        # Overall parent stats
        parent_stats = {
            'total_children': len(children_data),
            'total_courses': total_courses,
            'completed_courses': completed_courses,
            'total_assignments': total_assignments,
            'upcoming_assignments': upcoming_assignments,
        }

        data = {
            'children': children_data,
            'stats': parent_stats,
        }

        return Response(data)
