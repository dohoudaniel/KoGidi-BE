from django.urls import path
from .views import TeacherProfileView, TeacherProfileUpdateView

urlpatterns = [
    path('profile/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('profile/update/', TeacherProfileUpdateView.as_view(), name='teacher_profile_update'),
]
