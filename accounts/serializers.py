from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from students.models import Student
from teachers.models import Teacher
from parents.models import Parent

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'resident_state',
                  'is_student', 'is_teacher', 'is_parent', 'date_joined']
        read_only_fields = ['id', 'date_joined',
                            'is_student', 'is_teacher', 'is_parent']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    is_student = serializers.BooleanField(required=False, default=False)
    is_teacher = serializers.BooleanField(required=False, default=False)
    is_parent = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name',
                  'resident_state', 'is_student', 'is_teacher', 'is_parent']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 from validated data
        validated_data.pop('password2')

        # Get user type from context (query parameter)
        user_type = self.context.get('user_type', None)

        # Get user type flags from validated data
        is_student = validated_data.pop('is_student', False)
        is_teacher = validated_data.pop('is_teacher', False)
        is_parent = validated_data.pop('is_parent', False)

        # Override flags based on query parameter if provided
        if user_type == 'student':
            is_student = True
            is_teacher = False
            is_parent = False
        elif user_type == 'teacher':
            is_student = False
            is_teacher = True
            is_parent = False
        elif user_type == 'parent':
            is_student = False
            is_teacher = False
            is_parent = True

        # Create user with appropriate type flags
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            resident_state=validated_data['resident_state'],
            password=validated_data['password'],
            is_student=is_student,
            is_teacher=is_teacher,
            is_parent=is_parent
        )

        # Create corresponding profile based on user type
        if is_student:
            Student.objects.create(user=user)
        if is_teacher:
            Teacher.objects.create(user=user)
        if is_parent:
            Parent.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        return attrs
