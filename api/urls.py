from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from courses.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students',StudentViewset,basename='student')
router.register('courses',CourseViewset,basename='course')

urlpatterns = [
    path('token/refresh',TokenRefreshView.as_view()),
    path('token',TokenObtainPairView.as_view()),
    path('',include(router.urls)),
]
