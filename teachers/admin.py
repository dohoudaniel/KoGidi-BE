from django.contrib import admin
from .models import Teacher, TeacherClass, TeacherStats


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """
    Admin for the Teacher model
    """
    list_display = ('id', 'get_full_name', 'subject_specialization',
                    'years_of_experience', 'created_at')
    list_filter = ('subject_specialization',
                   'years_of_experience', 'created_at')
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'subject_specialization')
    readonly_fields = ('created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(TeacherClass)
class TeacherClassAdmin(admin.ModelAdmin):
    """
    Admin for Teacher Classes
    """
    list_display = ('name', 'teacher', 'course', 'total_students', 'progress_percentage', 'last_activity')
    list_filter = ('created_at', 'last_activity')
    search_fields = ('name', 'teacher__email', 'course__title')
    readonly_fields = ('created_at', 'updated_at', 'last_activity')


@admin.register(TeacherStats)
class TeacherStatsAdmin(admin.ModelAdmin):
    """
    Admin for Teacher Statistics
    """
    list_display = ('teacher', 'total_students', 'active_courses', 'pending_assignments', 'average_class_score')
    search_fields = ('teacher__email',)
    readonly_fields = ('updated_at',)
