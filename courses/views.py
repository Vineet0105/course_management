from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import *
class StudentViewset(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class =  StudentSerializer

class CourseViewset(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class =  CourseSerializer