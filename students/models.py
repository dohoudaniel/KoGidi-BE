from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    """
    Student profile model linked to the User model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    grade_level = models.CharField(
        _('grade level'), max_length=20, blank=True, default='')
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    school_name = models.CharField(
        _('school name'), max_length=255, blank=True, default='')
    interests = models.TextField(_('interests'), blank=True, default='')

    # Additional student fields
    enrollment_date = models.DateField(
        _('enrollment date'), null=True, blank=True)
    student_id = models.CharField(
        _('student ID'), max_length=50, blank=True, default='')
    guardian_name = models.CharField(
        _('guardian name'), max_length=255, blank=True, default='')
    guardian_contact = models.CharField(
        _('guardian contact'), max_length=100, blank=True, default='')
    emergency_contact = models.CharField(
        _('emergency contact'), max_length=100, blank=True, default='')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

    def __str__(self):
        return f"{self.user.get_full_name()} - Student"
