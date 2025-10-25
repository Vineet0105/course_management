from django.db import models
from django.contrib.auth.models import User
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE)
   
    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    students = models.ManyToManyField(Student, related_name='courses', blank=True)

    def __str__(self):
        return self.title