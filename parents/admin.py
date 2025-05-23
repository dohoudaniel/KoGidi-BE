from django.contrib import admin
from .models import Parent, ParentStudentRelationship


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """
    Admin for the Parent model
    """
    list_display = ('id', 'get_full_name', 'phone_number',
                    'occupation', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(ParentStudentRelationship)
class ParentStudentRelationshipAdmin(admin.ModelAdmin):
    """
    Admin for the ParentStudentRelationship model
    """
    list_display = ('id', 'get_parent_name', 'get_student_name',
                    'relationship', 'is_primary', 'created_at')
    list_filter = ('relationship', 'is_primary', 'created_at')
    search_fields = ('parent__user__email', 'parent__user__first_name', 'parent__user__last_name',
                     'student__user__email', 'student__user__first_name', 'student__user__last_name')

    def get_parent_name(self, obj):
        return obj.parent.user.get_full_name()
    get_parent_name.short_description = 'Parent'

    def get_student_name(self, obj):
        return obj.student.user.get_full_name()
    get_student_name.short_description = 'Student'
