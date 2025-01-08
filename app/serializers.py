from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
import re
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser

        return token


class RegistraionSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, data):
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Username already exists, enter a new one"}
            )

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists, enter a new one"}
            )

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"password_error": "Password doesn't match"}
            )

        if len(data["password"]) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long"}
            )

        if not re.search(r"[A-Z]", data["password"]):
            raise serializers.ValidationError(
                {"password": "Password must contain  one capital letter"}
            )

        if not re.search(r"\d", data["password"]):
            raise serializers.ValidationError(
                {"password": "Password must contain  one digit"}
            )

        if not re.search(r"[@$!%*?&#]", data["password"]):
            raise serializers.ValidationError(
                {"password": "Password must contain  one spcial character"}
            )

        return data

    def validate_username(self, value):
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores"
            )
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long"
            )
        return value


class TaskSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "status",
            "created_by",
            "users",
        ]
        read_only_fields = ["created_at", "created_by"]

    def get_users(self, obj):
        return [user.username for user in obj.users.all()]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
