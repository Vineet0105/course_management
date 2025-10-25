from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
class StudentViewset(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class =  StudentSerializer

class CourseViewset(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class =  CourseSerializer

    @action(detail=True, methods=['post'], url_path='add-student/(?P<student_id>[^/.]+)')
    def add_student(self, request, pk=None, student_id=None):
        """
        Add a student to the course.
        URL: POST /api/course/<course_id>/add-student/<student_id>/
        """
        course = self.get_object()

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        course.students.add(student)
        course.save()

        serializer = self.get_serializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
        