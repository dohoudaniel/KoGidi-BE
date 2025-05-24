from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    TokenRefreshView, UserProfileView
)

urlpatterns = [
    # API v1 endpoints
    path('v1/auth/signup/', RegisterView.as_view(), name='register'),
    path('v1/auth/login/', LoginView.as_view(), name='login'),
    path('v1/auth/logout/', LogoutView.as_view(), name='logout'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/profile/', UserProfileView.as_view(), name='user_profile'),
]
