from rest_framework import serializers
from .models import Parent, ParentStudentRelationship
from accounts.serializers import UserSerializer
from students.serializers import StudentSerializer


class ParentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Parent model
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Parent
        fields = ['id', 'user', 'phone_number', 'address', 'occupation', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ParentProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating parent profile
    """
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    resident_state = serializers.CharField(source='user.resident_state', required=False)
    
    class Meta:
        model = Parent
        fields = ['phone_number', 'address', 'occupation', 
                  'first_name', 'last_name', 'resident_state']
    
    def update(self, instance, validated_data):
        # Update User model fields if provided
        user_data = validated_data.pop('user', {})
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Update Parent model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class ParentStudentRelationshipSerializer(serializers.ModelSerializer):
    """
    Serializer for the ParentStudentRelationship model
    """
    parent = ParentSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    
    class Meta:
        model = ParentStudentRelationship
        fields = ['id', 'parent', 'student', 'relationship', 'is_primary', 'created_at']
        read_only_fields = ['id', 'parent', 'created_at']
