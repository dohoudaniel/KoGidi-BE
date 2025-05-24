from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


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
        _('subject specialization'), max_length=100, blank=True, default='')
    years_of_experience = models.PositiveIntegerField(
        _('years of experience'), default=0)
    qualification = models.CharField(
        _('qualification'), max_length=255, blank=True, default='')
    bio = models.TextField(_('biography'), blank=True, default='')

    # Additional teacher fields
    employee_id = models.CharField(
        _('employee ID'), max_length=50, blank=True, default='')
    department = models.CharField(
        _('department'), max_length=100, blank=True, default='')
    hire_date = models.DateField(_('hire date'), null=True, blank=True)
    teaching_level = models.CharField(
        _('teaching level'), max_length=50, blank=True, default='')
    certifications = models.TextField(
        _('certifications'), blank=True, default='')
    contact_number = models.CharField(
        _('contact number'), max_length=20, blank=True, default='')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    def __str__(self):
        return f"{self.user.get_full_name()} - Teacher"
