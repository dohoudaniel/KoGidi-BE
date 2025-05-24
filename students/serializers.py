from rest_framework import serializers
from .models import Student
from accounts.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'grade_level', 'date_of_birth', 'school_name',
            'interests', 'enrollment_date', 'student_id', 'guardian_name',
            'guardian_contact', 'emergency_contact', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating student profile
    """
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    resident_state = serializers.CharField(
        source='user.resident_state', required=False)

    class Meta:
        model = Student
        fields = [
            'grade_level', 'date_of_birth', 'school_name', 'interests',
            'enrollment_date', 'student_id', 'guardian_name', 'guardian_contact',
            'emergency_contact', 'first_name', 'last_name', 'resident_state'
        ]

    def update(self, instance, validated_data):
        # Update User model fields if provided
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Update Student model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
