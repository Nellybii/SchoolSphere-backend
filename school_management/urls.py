from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.userViews import (
    UserRegistrationView,
    UserViewSet,
    SchoolOwnerViewSet,
    TeacherViewSet,
    StudentViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('school-owners', SchoolOwnerViewSet, basename='school-owner')
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
