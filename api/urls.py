from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('token/refresh',TokenRefreshView.as_view()),
    path('token',TokenObtainPairView.as_view()),
]