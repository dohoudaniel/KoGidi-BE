from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Parent(models.Model):
    """
    Parent profile model linked to the User model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parent_profile'
    )
    phone_number = models.CharField(_('phone number'), max_length=20)
    address = models.TextField(_('address'), blank=True)
    occupation = models.CharField(_('occupation'), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('parent')
        verbose_name_plural = _('parents')

    def __str__(self):
        return f"{self.user.get_full_name()} - Parent"


class ParentStudentRelationship(models.Model):
    """
    Model to establish relationship between parents and students
    """
    parent = models.ForeignKey(
        'Parent',
        on_delete=models.CASCADE,
        related_name='student_relationships'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='parent_relationships'
    )
    # e.g., "Father", "Mother", "Guardian"
    relationship = models.CharField(_('relationship'), max_length=50)
    is_primary = models.BooleanField(_('is primary guardian'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('parent-student relationship')
        verbose_name_plural = _('parent-student relationships')
        unique_together = ('parent', 'student')

    def __str__(self):
        return f"{self.parent.user.get_full_name()} - {self.relationship} of {self.student.user.get_full_name()}"
