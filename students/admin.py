from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin for the Student model
    """
    list_display = ('id', 'get_full_name', 'grade_level',
                    'school_name', 'created_at')
    list_filter = ('grade_level', 'created_at')
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'school_name')
    readonly_fields = ('created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
