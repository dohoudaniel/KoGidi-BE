from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q, Avg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course, StudentProgress, Assignment, Achievement, StudentStats
from .serializers import (
    CourseSerializer, StudentProgressSerializer, AssignmentSerializer,
    AchievementSerializer, StudentStatsSerializer, DashboardDataSerializer
)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Course model
    Provides list and retrieve actions for courses
    """
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter courses based on query parameters
        """
        queryset = super().get_queryset()
        
        # Filter by grade
        grade = self.request.query_params.get('grade', None)
        if grade:
            queryset = queryset.filter(grade=grade)
        
        # Filter by subject
        subject = self.request.query_params.get('subject', None)
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        
        # Filter by language
        language = self.request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(language__icontains=language)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(subject__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """
        Get courses the student has enrolled in
        """
        progress = StudentProgress.objects.filter(student=request.user).select_related('course')
        courses = [p.course for p in progress]
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)


class StudentProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StudentProgress model
    """
    serializer_class = StudentProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return progress only for the current user
        """
        if getattr(self, 'swagger_fake_view', False):
            return StudentProgress.objects.none()
        return StudentProgress.objects.filter(student=self.request.user).select_related('course')
    
    def perform_create(self, serializer):
        """
        Set the student to the current user when creating progress
        """
        serializer.save(student=self.request.user)


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Assignment model
    """
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return assignments for the current user
        """
        if getattr(self, 'swagger_fake_view', False):
            return Assignment.objects.none()
        queryset = Assignment.objects.filter(
            Q(student=self.request.user) | Q(student__isnull=True)
        ).select_related('course')
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('due_date')
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit an assignment
        """
        assignment = self.get_object()
        assignment.status = 'submitted'
        from django.utils import timezone
        assignment.submitted_at = timezone.now()
        assignment.save()
        
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Achievement model
    """
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return achievements only for the current user
        """
        if getattr(self, 'swagger_fake_view', False):
            return Achievement.objects.none()
        return Achievement.objects.filter(student=self.request.user)


class DashboardView(APIView):
    """
    Combined API view for dashboard data
    Returns all data needed for the dashboard in one request
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get all dashboard data for the authenticated user",
        responses={
            200: DashboardDataSerializer(),
            401: "Unauthorized"
        }
    )
    def get(self, request):
        """
        Get comprehensive dashboard data
        """
        user = request.user
        
        # Get or create student stats
        stats, created = StudentStats.objects.get_or_create(student=user)
        
        # If newly created, calculate initial stats
        if created:
            progress_records = StudentProgress.objects.filter(student=user)
            stats.total_courses = progress_records.count()
            stats.completed_courses = progress_records.filter(is_completed=True).count()
            stats.total_hours = sum(p.time_spent_minutes for p in progress_records) // 60
            avg_score = progress_records.aggregate(Avg('average_score'))['average_score__avg']
            stats.average_score = avg_score if avg_score else 0
            stats.save()
        
        # Get courses
        all_courses = Course.objects.filter(is_published=True)[:20]
        
        # Get recent courses (courses with progress)
        recent_progress = StudentProgress.objects.filter(
            student=user
        ).select_related('course').order_by('-last_accessed')[:4]
        recent_courses = [p.course for p in recent_progress]
        
        # Get assignments
        assignments = Assignment.objects.filter(
            Q(student=user) | Q(student__isnull=True)
        ).select_related('course').order_by('due_date')[:5]
        
        # Get achievements
        achievements = Achievement.objects.filter(student=user).order_by('-earned_at')[:10]
        
        # Get all progress
        progress = StudentProgress.objects.filter(student=user).select_related('course')
        
        # Serialize data
        context = {'request': request}
        data = {
            'stats': StudentStatsSerializer(stats).data,
            'courses': CourseSerializer(all_courses, many=True, context=context).data,
            'recent_courses': CourseSerializer(recent_courses, many=True, context=context).data,
            'assignments': AssignmentSerializer(assignments, many=True).data,
            'achievements': AchievementSerializer(achievements, many=True).data,
            'progress': StudentProgressSerializer(progress, many=True).data,
        }
        
        return Response(data)


class StudentStatsView(APIView):
    """
    API view for student statistics
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get student statistics
        """
        stats, created = StudentStats.objects.get_or_create(student=request.user)
        serializer = StudentStatsSerializer(stats)
        return Response(serializer.data)
