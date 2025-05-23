from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration

    This endpoint allows users to register as students, teachers, or parents.
    The user type is determined by the 'type' query parameter.

    Query Parameters:
    - type: The type of user to register (student, teacher, or parent)

    Request Body:
    - email: User's email address
    - password: User's password
    - password2: Password confirmation
    - first_name: User's first name
    - last_name: User's last name
    - resident_state: User's resident state

    Returns:
    - 201 Created: User registered successfully
    - 400 Bad Request: Invalid data provided
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Get user type from query parameters
        user_type = self.request.query_params.get('type', None)
        if user_type not in ['student', 'teacher', 'parent']:
            user_type = None
        context.update({"user_type": user_type})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Create response with tokens in cookies
        response = Response({
            "message": "User registered successfully",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

        # Set cookies
        response.set_cookie(
            'access_token',
            access_token,
            max_age=60 * 15,  # 15 minutes
            httponly=True,
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            samesite='Lax'
        )

        return response


class LoginView(APIView):
    """
    API view for user login

    This endpoint allows users to log in as students, teachers, or parents.
    The user type is determined by the 'type' query parameter.

    Query Parameters:
    - type: The type of user to log in as (student, teacher, or parent)

    Request Body:
    - email: User's email address
    - password: User's password

    Returns:
    - 200 OK: Login successful, with user data and tokens in cookies
    - 401 Unauthorized: Invalid credentials
    - 403 Forbidden: User type mismatch
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Get user type from query parameters
        user_type = request.query_params.get('type', None)

        # Authenticate user
        user = authenticate(email=email, password=password)

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if user type matches
        if user_type == 'student' and not user.is_student:
            return Response(
                {"error": "User is not registered as a student"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif user_type == 'teacher' and not user.is_teacher:
            return Response(
                {"error": "User is not registered as a teacher"},
                status=status.HTTP_403_FORBIDDEN
            )
        elif user_type == 'parent' and not user.is_parent:
            return Response(
                {"error": "User is not registered as a parent"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Create response with tokens in cookies
        response = Response({
            "message": "Login successful",
            "user": UserSerializer(user).data
        })

        # Set cookies
        response.set_cookie(
            'access_token',
            access_token,
            max_age=60 * 15,  # 15 minutes
            httponly=True,
            samesite='Lax'
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=60 * 60 * 24 * 7,  # 7 days
            httponly=True,
            samesite='Lax'
        )

        return response


class LogoutView(APIView):
    """
    API view for user logout

    This endpoint allows authenticated users to log out.
    It blacklists the refresh token and removes both access and refresh tokens from cookies.

    Returns:
    - 200 OK: Logout successful
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        # Create response and delete cookies
        response = Response({"message": "Logout successful"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class TokenRefreshView(APIView):
    """
    API view for refreshing access token

    This endpoint allows users to refresh their access token using the refresh token stored in cookies.

    Returns:
    - 200 OK: Token refreshed successfully, with new access token in cookies
    - 401 Unauthorized: Invalid or missing refresh token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Get refresh token from cookie
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {"error": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Verify and refresh token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            # Create response with new access token in cookie
            response = Response({"message": "Token refreshed successfully"})

            # Set new access token cookie
            response.set_cookie(
                'access_token',
                access_token,
                max_age=60 * 15,  # 15 minutes
                httponly=True,
                samesite='Lax'
            )

            return response
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserProfileView(generics.RetrieveAPIView):
    """
    API view for retrieving user profile

    This endpoint allows authenticated users to retrieve their profile information.

    Returns:
    - 200 OK: User profile data
    - 401 Unauthorized: User is not authenticated
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
