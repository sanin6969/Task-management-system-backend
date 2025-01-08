from rest_framework.views import APIView
from .serializers import (
    RegistraionSerializer,
    TaskSerializer,
    MyTokenObtainPairSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


@swagger_auto_schema(
    request_body=RegistraionSerializer,
    responses={200: openapi.Response("Registration successful")},
)
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistraionSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            return Response(
                {
                    "message": "Registration succesfull ",
                    "username": serializer.validated_data["username"],
                    "email": serializer.validated_data["email"],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response("List of tasks")},
    )
    def get(self, request):
        if request.user.is_superuser:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(users=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"Tasks": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TaskSerializer,
        responses={201: openapi.Response("Task created successfully")},
    )
    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {"only admin can create tasks"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(created_by=request.user)
            users = request.data.get("users", [])
            if users:
                task.users.set(users)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["work_in_progress", "completed", "declined"],
            ),
        },
    ),
    responses={200: openapi.Response("Status updated successfully")},
)
class TaskStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if task.status in ["pending", "work_in_progress"]:
            statuses = request.data.get("status")

            if statuses in ["work_in_progress", "completed", "declined"]:
                task.status = statuses
                task.save()
                return Response(
                    {"message": "Status updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"error": "Task cannot be updated"}, status=status.HTTP_400_BAD_REQUEST
        )


@swagger_auto_schema(
    responses={200: openapi.Response("List of users")},
)
class ListAllUsers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(is_superuser=False)
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)
