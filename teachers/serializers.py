from rest_framework import serializers
from .models import Teacher
from accounts.serializers import UserSerializer


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Teacher model
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'subject_specialization', 'years_of_experience', 
                  'qualification', 'bio', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating teacher profile
    """
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    resident_state = serializers.CharField(source='user.resident_state', required=False)
    
    class Meta:
        model = Teacher
        fields = ['subject_specialization', 'years_of_experience', 'qualification', 
                  'bio', 'first_name', 'last_name', 'resident_state']
    
    def update(self, instance, validated_data):
        # Update User model fields if provided
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Update Teacher model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
