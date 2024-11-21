from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from ..models import SchoolOwner, Teacher, Student
from ..serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    SchoolOwnerSerializer,
    TeacherSerializer,
    StudentSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class SchoolOwnerViewSet(viewsets.ModelViewSet):
    queryset = SchoolOwner.objects.all()
    serializer_class = SchoolOwnerSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
