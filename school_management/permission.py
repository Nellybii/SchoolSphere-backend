from rest_framework import permissions


class IsSchoolOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_school_owner

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student
