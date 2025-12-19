from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from courses.models import Course


class Teacher(models.Model):
    """
    Teacher profile model linked to the User model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    subject_specialization = models.CharField(
        _('subject specialization'), max_length=255, blank=True, default='')
    years_of_experience = models.IntegerField(
        _('years of experience'), default=0)
    qualification = models.CharField(
        _('qualification'), max_length=255, blank=True, default='')
    bio = models.TextField(_('bio'), blank=True, default='')

    # Additional teacher fields
    employee_id = models.CharField(
        _('employee ID'), max_length=50, blank=True, default='')
    department = models.CharField(
        _('department'), max_length=100, blank=True, default='')
    office_location = models.CharField(
        _('office location'), max_length=255, blank=True, default='')
    contact_hours = models.CharField(
        _('contact hours'), max_length=255, blank=True, default='')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    def __str__(self):
        return f"{self.user.get_full_name()} - Teacher"


class TeacherClass(models.Model):
    """
    Classes managed by teachers
    """
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_classes'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='teacher_classes'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_students = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    progress_percentage = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Teacher Class'
        verbose_name_plural = 'Teacher Classes'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.name} - {self.teacher.email}"


class TeacherStats(models.Model):
    """
    Aggregate statistics for teachers
    """
    teacher = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_stats'
    )
    
    total_students = models.IntegerField(default=0)
    active_courses = models.IntegerField(default=0)
    pending_assignments = models.IntegerField(default=0)
    average_class_score = models.FloatField(default=0.0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Teacher Stats'
        verbose_name_plural = 'Teacher Stats'
    
    def __str__(self):
        return f"Stats for {self.teacher.email}"
