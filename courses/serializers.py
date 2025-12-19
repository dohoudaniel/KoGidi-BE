from rest_framework import serializers
from .models import Course, StudentProgress, Assignment, Achievement, StudentStats


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """
    lessons = serializers.IntegerField(source='total_lessons', read_only=True)
    isDownloaded = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'subject', 'grade', 'level',
            'language', 'duration', 'category', 'thumbnail', 'lessons',
            'total_lessons', 'isDownloaded', 'progress', 'created_at'
        ]
    
    def get_isDownloaded(self, obj):
        """Check if course is downloaded for the current user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if user has started this course
            return StudentProgress.objects.filter(
                student=request.user,
                course=obj
            ).exists()
        return False
    
    def get_progress(self, obj):
        """Get user's progress in this course"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = StudentProgress.objects.filter(
                student=request.user,
                course=obj
            ).first()
            if progress:
                return progress.progress_percentage
        return 0


class StudentProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentProgress model
    """
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StudentProgress
        fields = [
            'id', 'course', 'course_id', 'progress_percentage',
            'completed_lessons', 'time_spent_minutes', 'last_accessed',
            'is_completed', 'average_score', 'started_at', 'completed_at'
        ]
        read_only_fields = ['started_at', 'last_accessed']


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Assignment model
    """
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'course', 'course_title', 'title', 'description',
            'priority', 'status', 'due_date', 'submitted_at', 'score',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for Achievement model
    """
    date = serializers.DateTimeField(source='earned_at', read_only=True)
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'title', 'description', 'achievement_type',
            'icon', 'earned_at', 'date'
        ]
        read_only_fields = ['earned_at']


class StudentStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentStats model
    """
    class Meta:
        model = StudentStats
        fields = [
            'total_courses', 'completed_courses', 'current_streak',
            'total_hours', 'average_score', 'last_activity'
        ]
        read_only_fields = ['last_activity']


class DashboardDataSerializer(serializers.Serializer):
    """
    Combined serializer for dashboard data
    """
    stats = StudentStatsSerializer(read_only=True)
    courses = CourseSerializer(many=True, read_only=True)
    recent_courses = CourseSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)
    progress = StudentProgressSerializer(many=True, read_only=True)
