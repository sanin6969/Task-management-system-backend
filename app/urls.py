from .views import *
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
schema_view = get_schema_view(
    openapi.Info(
        title="Task Management",
        default_version='v1',
        description="API for Task Management",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path("register/", UserRegistrationView.as_view(),name='register'),
    path("task/", TaskView.as_view(),name='task'),
    path("users/", ListAllUsers.as_view(),name='users'),
    path('task/<int:task_id>/', TaskStatusUpdateView.as_view(), name='task_status_update'),
]