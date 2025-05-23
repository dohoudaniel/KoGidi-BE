from django.urls import path
from .views import ParentProfileView, ParentProfileUpdateView

urlpatterns = [
    path('profile/', ParentProfileView.as_view(), name='parent_profile'),
    path('profile/update/', ParentProfileUpdateView.as_view(), name='parent_profile_update'),
]
