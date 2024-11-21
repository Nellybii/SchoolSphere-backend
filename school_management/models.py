from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_school_owner = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class SchoolOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True) 

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schools')

    def __str__(self):
        return self.name

class Stream(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=50)
    number_of_students = models.PositiveIntegerField(default=0)
    subjects = models.ManyToManyField('Subject', related_name='classes')
    class_teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_teacher')
    streams = models.ManyToManyField(Stream, related_name='classes')

    def __str__(self):
        return f"{self.name} - {self.school.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    guardian_name = models.CharField(max_length=255)
    guardian_contact = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.full_name} - {self.school.name}"

class Account(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='account')
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.balance = self.total_fees - self.amount_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - Balance: {self.balance}"
