from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """
    Course model representing learning content
    """
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    GRADE_CHOICES = [
        ('primary_1', 'Primary 1'),
        ('primary_2', 'Primary 2'),
        ('primary_3', 'Primary 3'),
        ('primary_4', 'Primary 4'),
        ('primary_5', 'Primary 5'),
        ('primary_6', 'Primary 6'),
        ('jss_1', 'JSS 1'),
        ('jss_2', 'JSS 2'),
        ('jss_3', 'JSS 3'),
        ('sss_1', 'SSS 1'),
        ('sss_2', 'SSS 2'),
        ('sss_3', 'SSS 3'),
    ]
    
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    subject = models.CharField(_('subject'), max_length=100)
    grade = models.CharField(_('grade'), max_length=50, choices=GRADE_CHOICES)
    level = models.CharField(_('level'), max_length=50, choices=LEVEL_CHOICES, default='beginner')
    language = models.CharField(_('language'), max_length=50, default='English')
    duration = models.CharField(_('duration'), max_length=50, help_text='e.g., 4 weeks')
    category = models.CharField(_('category'), max_length=100)
    thumbnail = models.URLField(_('thumbnail'), blank=True, default='/placeholder.svg')
    
    # Course content
    total_lessons = models.IntegerField(_('total lessons'), default=0)
    is_published = models.BooleanField(_('is published'), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subject']),
            models.Index(fields=['grade']),
            models.Index(fields=['level']),
            models.Index(fields=['is_published']),
            models.Index(fields=['subject', 'grade']),
        ]
    
    def __str__(self):
        return self.title


class StudentProgress(models.Model):
    """
    Track student progress in courses
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_progress'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )
    
    progress_percentage = models.IntegerField(_('progress percentage'), default=0)
    completed_lessons = models.IntegerField(_('completed lessons'), default=0)
    time_spent_minutes = models.IntegerField(_('time spent (minutes)'), default=0)
    last_accessed = models.DateTimeField(_('last accessed'), auto_now=True)
    is_completed = models.BooleanField(_('is completed'), default=False)
    
    # Performance metrics
    average_score = models.FloatField(_('average score'), default=0.0)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('student progress')
        verbose_name_plural = _('student progress')
        unique_together = ['student', 'course']
        ordering = ['-last_accessed']
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['is_completed']),
            models.Index(fields=['last_accessed']),
        ]
    
    def __str__(self):
        return f"{self.student.email} - {self.course.title} ({self.progress_percentage}%)"


class Assignment(models.Model):
    """
    Assignments and quizzes for courses
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True
    )
    
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    priority = models.CharField(_('priority'), max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    due_date = models.DateField(_('due date'))
    submitted_at = models.DateTimeField(_('submitted at'), null=True, blank=True)
    score = models.FloatField(_('score'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')
        ordering = ['due_date', '-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['course']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Achievement(models.Model):
    """
    Student achievements and badges
    """
    ACHIEVEMENT_TYPES = [
        ('course_completion', 'Course Completion'),
        ('streak', 'Learning Streak'),
        ('score', 'High Score'),
        ('milestone', 'Milestone'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    achievement_type = models.CharField(_('type'), max_length=50, choices=ACHIEVEMENT_TYPES)
    icon = models.CharField(_('icon'), max_length=10, default='🏆')
    
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('achievement')
        verbose_name_plural = _('achievements')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.title}"


class StudentStats(models.Model):
    """
    Aggregate statistics for students
    """
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stats'
    )
    
    total_courses = models.IntegerField(_('total courses'), default=0)
    completed_courses = models.IntegerField(_('completed courses'), default=0)
    current_streak = models.IntegerField(_('current streak (days)'), default=0)
    total_hours = models.IntegerField(_('total hours'), default=0)
    average_score = models.FloatField(_('average score'), default=0.0)
    
    last_activity = models.DateTimeField(_('last activity'), auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('student stats')
        verbose_name_plural = _('student stats')
    
    def __str__(self):
        return f"Stats for {self.student.email}"
