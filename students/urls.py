from django.urls import path
from .views import StudentProfileView, StudentProfileUpdateView

urlpatterns = [
    path('profile/', StudentProfileView.as_view(), name='student_profile'),
    path('profile/update/', StudentProfileUpdateView.as_view(), name='student_profile_update'),
]
