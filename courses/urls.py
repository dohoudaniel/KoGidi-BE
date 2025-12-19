from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, StudentProgressViewSet, AssignmentViewSet,
    AchievementViewSet, DashboardView, StudentStatsView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'progress', StudentProgressViewSet, basename='progress')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'achievements', AchievementViewSet, basename='achievement')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('stats/', StudentStatsView.as_view(), name='student-stats'),
    path('', include(router.urls)),
]
