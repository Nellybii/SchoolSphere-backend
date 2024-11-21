import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SchoolOwner, Teacher, Student

logger = logging.getLogger(__name__)

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user_type = serializers.ChoiceField(choices=['school_owner', 'teacher', 'student'])
    
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    contact_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'user_type', 'first_name', 'last_name', 'contact_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """Validate that passwords match"""
        logger.debug("Validating data: %s", data)

        if data['password'] != data['password2']:
            logger.error("Passwords do not match: %s, %s", data['password'], data['password2'])
            raise serializers.ValidationError({'password': 'Passwords must match'})
        
        logger.debug("Password validation passed")
        return data

    def create(self, validated_data):
        """Create user and corresponding profile based on user_type"""
        user_type = validated_data.pop('user_type')  
        validated_data.pop('password2') 

        user_data = {key: validated_data[key] for key in ['username', 'email', 'password']}
        user = User.objects.create_user(**user_data)

        if user_type == 'school_owner':
            school_owner = SchoolOwner.objects.create(
                user=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                contact_number=validated_data['contact_number'],
                email=validated_data['email']
            )
            logger.debug("SchoolOwner profile created for user: %s", user.username)
        elif user_type == 'teacher':
            teacher = Teacher.objects.create(
                user=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                contact=validated_data['contact_number'],
                email=validated_data['email']
            )
            logger.debug("Teacher profile created for user: %s", user.username)
        elif user_type == 'student':
            student = Student.objects.create(
                user=user,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                contact_number=validated_data['contact_number'],
                email=validated_data['email'],
                full_name=f"{validated_data['first_name']} {validated_data['last_name']}"  
            )
            logger.debug("Student profile created for user: %s", user.username)

        logger.debug("User and profile created successfully: %s", user.username)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer to display User data"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class SchoolOwnerSerializer(serializers.ModelSerializer):
    """Serializer for SchoolOwner profile"""
    user = UserSerializer()

    class Meta:
        model = SchoolOwner
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher profile"""
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student profile"""
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'
