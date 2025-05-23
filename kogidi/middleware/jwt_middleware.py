from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser


def get_user(request):
    """
    Get the user from the JWT token in the cookie
    """
    token = request.COOKIES.get('access_token')
    if not token:
        return AnonymousUser()
    
    auth = JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(token)
        user, _ = auth.get_user(validated_token), validated_token
        return user
    except AuthenticationFailed:
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Middleware to authenticate users via JWT token in cookies
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view is called
        if not hasattr(request, 'user') or request.user.is_anonymous:
            request.user = SimpleLazyObject(lambda: get_user(request))
        
        # Call the view
        response = self.get_response(request)
        
        # Process the response
        return response
