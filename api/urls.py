from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from courses.views import *
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from accounts.views import *

router = DefaultRouter()
router.register('students',StudentViewset,basename='student')
router.register('courses',CourseViewset,basename='course')

schema_view = get_schema_view(
   openapi.Info(
      title="Course API",
      default_version='v1',
      description="API documentation for our project",
      terms_of_service="https://www.google.com/terms/",
      contact=openapi.Contact(email="abc@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('token/refresh',TokenRefreshView.as_view()),
    path('token',TokenObtainPairView.as_view()),
    path('',include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register',RegisterAPIView.as_view())

]
