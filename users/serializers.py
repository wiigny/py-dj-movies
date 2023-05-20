from rest_framework import serializers
from users.models import User
from users.exceptions import UniqueUserNameOrEmail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import ipdb


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_employee"] = user.is_employee

        return token


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(max_length=20)
    email = serializers.CharField(max_length=127)
    birthdate = serializers.DateField(required=False, default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_employee = serializers.BooleanField(required=False, default=False)

    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        username = User.objects.filter(username__iexact=validated_data["username"])
        email = User.objects.filter(email__iexact=validated_data["email"])
        if username or email:
            raise UniqueUserNameOrEmail(
                {
                    "username": ["username already taken."],
                    "email": ["email already registered."],
                }
            )

        if not validated_data["is_employee"]:
            return User.objects.create_user(**validated_data)
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if validated_data["password"]:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance
