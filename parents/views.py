from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Parent, ParentStudentRelationship
from .serializers import ParentSerializer, ParentProfileUpdateSerializer, ParentStudentRelationshipSerializer


class IsParentUser(IsAuthenticated):
    """
    Custom permission to only allow parents to access their own profile

    This permission class checks if:
    1. The user is authenticated
    2. The user has a parent profile
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, 'parent_profile')


class ParentProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving parent profile

    This endpoint allows authenticated parent users to retrieve their profile information.

    Returns:
    - 200 OK: Parent profile data
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a parent
    """
    serializer_class = ParentSerializer
    permission_classes = [IsParentUser]

    def get_object(self):
        return self.request.user.parent_profile


class ParentProfileUpdateView(generics.UpdateAPIView):
    """
    API view for updating parent profile

    This endpoint allows authenticated parent users to update their profile information.

    Request Body:
    - phone_number: Parent's phone number (optional)
    - address: Parent's address (optional)
    - occupation: Parent's occupation (optional)
    - first_name: Parent's first name (optional)
    - last_name: Parent's last name (optional)
    - resident_state: Parent's resident state (optional)

    Returns:
    - 200 OK: Parent profile updated successfully
    - 400 Bad Request: Invalid data provided
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a parent
    """
    serializer_class = ParentProfileUpdateSerializer
    permission_classes = [IsParentUser]

    def get_object(self):
        return self.request.user.parent_profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(ParentSerializer(instance).data)
