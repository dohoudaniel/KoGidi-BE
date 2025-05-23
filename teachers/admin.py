from django.contrib import admin
from .models import Teacher


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
