from django.contrib import admin
from .models import Course, StudentProgress, Assignment, Achievement, StudentStats


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'grade', 'level', 'total_lessons', 'is_published', 'created_at']
    list_filter = ['grade', 'subject', 'level', 'is_published', 'language']
    search_fields = ['title', 'description', 'subject']
    ordering = ['-created_at']


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress_percentage', 'is_completed', 'last_accessed']
    list_filter = ['is_completed', 'course__grade', 'course__subject']
    search_fields = ['student__email', 'course__title']
    readonly_fields = ['started_at', 'last_accessed']
    ordering = ['-last_accessed']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'student', 'priority', 'status', 'due_date', 'score']
    list_filter = ['priority', 'status', 'course']
    search_fields = ['title', 'course__title', 'student__email']
    ordering = ['due_date', '-created_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'achievement_type', 'icon', 'earned_at']
    list_filter = ['achievement_type', 'earned_at']
    search_fields = ['title', 'student__email']
    ordering = ['-earned_at']


@admin.register(StudentStats)
class StudentStatsAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_courses', 'completed_courses', 'current_streak', 'total_hours', 'average_score']
    search_fields = ['student__email']
    readonly_fields = ['last_activity', 'updated_at']
