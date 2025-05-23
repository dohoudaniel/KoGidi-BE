from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Teacher
from .serializers import TeacherSerializer, TeacherProfileUpdateSerializer


class IsTeacherUser(IsAuthenticated):
    """
    Custom permission to only allow teachers to access their own profile

    This permission class checks if:
    1. The user is authenticated
    2. The user has a teacher profile
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, 'teacher_profile')


class TeacherProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving teacher profile

    This endpoint allows authenticated teacher users to retrieve their profile information.

    Returns:
    - 200 OK: Teacher profile data
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a teacher
    """
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacherUser]

    def get_object(self):
        return self.request.user.teacher_profile


class TeacherProfileUpdateView(generics.UpdateAPIView):
    """
    API view for updating teacher profile

    This endpoint allows authenticated teacher users to update their profile information.

    Request Body:
    - subject_specialization: Teacher's subject specialization (optional)
    - years_of_experience: Teacher's years of experience (optional)
    - qualification: Teacher's qualification (optional)
    - bio: Teacher's biography (optional)
    - first_name: Teacher's first name (optional)
    - last_name: Teacher's last name (optional)
    - resident_state: Teacher's resident state (optional)

    Returns:
    - 200 OK: Teacher profile updated successfully
    - 400 Bad Request: Invalid data provided
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a teacher
    """
    serializer_class = TeacherProfileUpdateSerializer
    permission_classes = [IsTeacherUser]

    def get_object(self):
        return self.request.user.teacher_profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(TeacherSerializer(instance).data)
