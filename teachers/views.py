from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Teacher, TeacherClass, TeacherStats
from .serializers import TeacherSerializer, TeacherProfileUpdateSerializer
from courses.models import Course, Assignment
from courses.serializers import CourseSerializer, AssignmentSerializer


class IsTeacherUser(IsAuthenticated):
    """
    Custom permission to only allow teachers to access their own profile

    This permission class checks if:
    1. The user is authenticated
    2. The user has a teacher profile
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, 'teacher_profile')


class TeacherProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving teacher profile

    This endpoint allows authenticated teacher users to retrieve their profile information.

    Returns:
    - 200 OK: Teacher profile data
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a teacher
    """
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacherUser]

    @swagger_auto_schema(
        responses={
            200: TeacherSerializer,
            401: "User is not authenticated",
            403: "User is not a teacher"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.teacher_profile


class TeacherProfileUpdateView(generics.UpdateAPIView):
    """
    API view for updating teacher profile

    This endpoint allows authenticated teacher users to update their profile information.

    Request Body:
    - subject_specialization: Teacher's subject specialization (optional)
    - years_of_experience: Teacher's years of experience (optional)
    - qualification: Teacher's qualification (optional)
    - bio: Teacher's biography (optional)
    - first_name: Teacher's first name (optional)
    - last_name: Teacher's last name (optional)
    - resident_state: Teacher's resident state (optional)

    Returns:
    - 200 OK: Teacher profile updated successfully
    - 400 Bad Request: Invalid data provided
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a teacher
    """
    serializer_class = TeacherProfileUpdateSerializer
    permission_classes = [IsTeacherUser]

    def get_object(self):
        return self.request.user.teacher_profile

    @swagger_auto_schema(
        request_body=TeacherProfileUpdateSerializer,
        responses={
            200: TeacherSerializer,
            400: "Invalid data provided",
            401: "User is not authenticated",
            403: "User is not a teacher"
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(TeacherSerializer(instance).data)


class TeacherDashboardView(APIView):
    """
    Combined API view for teacher dashboard data
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all dashboard data for authenticated teacher",
        responses={
            200: "Dashboard data",
            401: "Unauthorized"
        }
    )
    def get(self, request):
        """
        Get comprehensive teacher dashboard data
        """
        user = request.user

        # Check if user is a teacher
        if not hasattr(user, 'teacher_profile'):
            return Response(
                {'error': 'Only teachers can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get or create teacher stats
        teacher_stats, created = TeacherStats.objects.get_or_create(teacher=user)

        # If newly created, calculate initial stats
        if created or True:  # Always recalculate for now
            classes = TeacherClass.objects.filter(teacher=user)
            teacher_stats.active_courses = classes.count()
            teacher_stats.total_students = sum(c.total_students for c in classes)
            
            # Count pending assignments (assignments not graded)
            pending = Assignment.objects.filter(
                course__teacher_classes__teacher=user,
                status='submitted'
            ).count()
            teacher_stats.pending_assignments = pending
            
            # Calculate average class score
            teacher_stats.average_class_score = 78.0  # Mock for now
            teacher_stats.save()

        # Get classes
        classes = TeacherClass.objects.filter(teacher=user).select_related('course')
        
        # Get pending grading assignments
        pending_grading = Assignment.objects.filter(
            course__teacher_classes__teacher=user,
            status='submitted'
        ).select_related('course', 'student')[:10]

        # Serialize data
        stats_data = {
            'total_students': teacher_stats.total_students,
            'active_courses': teacher_stats.active_courses,
            'pending_assignments': teacher_stats.pending_assignments,
            'average_class_score': teacher_stats.average_class_score,
        }

        classes_data = [{
            'id': cls.id,
            'name': cls.name,
            'students': cls.total_students,
            'lastActivity': cls.last_activity.strftime('%Y-%m-%d %H:%M'),
            'progress': cls.progress_percentage,
        } for cls in classes]

        pending_data = AssignmentSerializer(pending_grading, many=True).data

        data = {
            'stats': stats_data,
            'recent_classes': classes_data,
            'pending_grading': pending_data,
            'upcoming_lessons': [],  # Placeholder for future implementation
        }

        return Response(data)
