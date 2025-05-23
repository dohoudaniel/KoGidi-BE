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
        _('subject specialization'), max_length=100)
    years_of_experience = models.PositiveIntegerField(
        _('years of experience'), default=0)
    qualification = models.CharField(_('qualification'), max_length=255)
    bio = models.TextField(_('biography'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    def __str__(self):
        return f"{self.user.get_full_name()} - Teacher"
