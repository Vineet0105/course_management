from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

class StudentViewset(ModelViewSet):
    # queryset = Student.objects.all()
    serializer_class =  StudentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CourseViewset(ModelViewSet):
    serializer_class =  CourseSerializer
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields  = ['title']

    @action(detail=True, methods=['post'], url_path='add-student/(?P<student_id>[^/.]+)')
    def add_student(self, request, pk=None, student_id=None):
        """
        Add a student to the course.
        URL: POST /api/course/<course_id>/add-student/<student_id>/
        """
        course = self.get_object()
        ids = student_id.split(',')
        for i in ids:
            try:
                Student.objects.filter(pk=i, user=request.user).first()
                Student.objects.get(pk=i)
            except Student.DoesNotExist:
                return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

            course.students.add(student)
            course.save()

        serializer = self.get_serializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    @action(detail=True,methods=['post'],url_path='remove-student/(?P<student_id>[^/.]+)')
    def remove_student(self,request,pk,student_id):
        course = self.get_object()
        ids = student_id.split(',')
        for i in ids:
            try:
                course.students.get(pk=int(i))
            except:
                return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
            
            student = Student.objects.get(pk=int(i))
            course.students.remove(student)
            course.save()

        serializer = self.get_serializer(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    