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
    grade_level = models.CharField(_('grade level'), max_length=20)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    school_name = models.CharField(
        _('school name'), max_length=255, blank=True)
    interests = models.TextField(_('interests'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

    def __str__(self):
        return f"{self.user.get_full_name()} - Student"
