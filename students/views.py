from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Student
from .serializers import StudentSerializer, StudentProfileUpdateSerializer


class IsStudentUser(IsAuthenticated):
    """
    Custom permission to only allow students to access their own profile

    This permission class checks if:
    1. The user is authenticated
    2. The user has a student profile
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and hasattr(request.user, 'student_profile')


class StudentProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving student profile

    This endpoint allows authenticated student users to retrieve their profile information.

    Returns:
    - 200 OK: Student profile data
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a student
    """
    serializer_class = StudentSerializer
    permission_classes = [IsStudentUser]

    @swagger_auto_schema(
        responses={
            200: StudentSerializer,
            401: "User is not authenticated",
            403: "User is not a student"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.student_profile


class StudentProfileUpdateView(generics.UpdateAPIView):
    """
    API view for updating student profile

    This endpoint allows authenticated student users to update their profile information.

    Request Body:
    - grade_level: Student's grade level (optional)
    - date_of_birth: Student's date of birth (optional)
    - school_name: Student's school name (optional)
    - interests: Student's interests (optional)
    - first_name: Student's first name (optional)
    - last_name: Student's last name (optional)
    - resident_state: Student's resident state (optional)

    Returns:
    - 200 OK: Student profile updated successfully
    - 400 Bad Request: Invalid data provided
    - 401 Unauthorized: User is not authenticated
    - 403 Forbidden: User is not a student
    """
    serializer_class = StudentProfileUpdateSerializer
    permission_classes = [IsStudentUser]

    def get_object(self):
        return self.request.user.student_profile

    @swagger_auto_schema(
        request_body=StudentProfileUpdateSerializer,
        responses={
            200: StudentSerializer,
            400: "Invalid data provided",
            401: "User is not authenticated",
            403: "User is not a student"
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(StudentSerializer(instance).data)
