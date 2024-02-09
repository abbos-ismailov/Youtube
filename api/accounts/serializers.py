from typing import Any, Dict
from rest_framework import serializers, generics
from api.accounts.models import User
from django.core.validators import FileExtensionValidator
from api.base.utility import send_email, check_username, check_user
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import models
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt import tokens
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    ### The hereto function is for new field adding
    # def __init__(self, *args, **kwargs):
    #     super(SignUpSerializer, self).__init__(*args, **kwargs)
    #     self.fields["email_or_phone"] = serializers.CharField(required=True)

    ### the hereto code is for adding new (read_only=True)
    # auth_status = serializers.CharField(read_only=True, required=True)
    class Meta:
        model = User
        fields = ("id", "auth_status", "email")  ### these is returned fields
        extra_kwargs = {
            "id": {"read_only": True},
            "auth_status": {"read_only": True, "required": True},
        }

    def create(self, validated_data):
        user = super(SignupSerializer, self).create(validated_data)
        code = user.create_code()
        send_email(user.email, code=code)
        user.save()
        return user

    def to_representation(self, instance):
        data = super(SignupSerializer, self).to_representation(instance)
        data.update(instance.token())

        return data


class PersonalDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    photo = serializers.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
            )
        ]
    )

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get("password", None)
        confirm_password = data.get("confirm_password")

        if password:
            validate_password(password=password)

        if password != confirm_password:
            data = {"status": False, "message": "Parollar bir biriga mos emas"}
            raise ValidationError(data)
        return data

    def validate_username(self, username):
        if not check_username(username):
            data = {"status": False, "message": "Bu username yaroqsiz"}
            raise ValidationError(data)
        if User.objects.filter(username=username).exists():
            data = {"status": False, "message": "Bu username bor"}
            raise ValidationError(data)
        return username

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.password = validated_data.get("password", instance.password)

        if validated_data.get("password"):
            instance.set_password(validated_data.get("password"))
        instance.photo = validated_data.get("photo", instance.photo)

        if instance.auth_status == "verify_code":
            instance.auth_status = "complate"
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    # trying_count = serializers.IntegerField(default=0, required=False, read_only=True)
    def __init__(self, *args, **kwargs) -> None:
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields["username"] = serializers.CharField(required=False, read_only=True)
        self.fields["user_input"] = serializers.CharField(required=True)
        # self.fields["trying_count"] = serializers.IntegerField(default=0, required=False)

    def auth_validate(self, data):
        user_input = data.get("user_input")
        password = data.get("password")

        if check_user(user_input) == "email":
            username = self.auth_by_email(user_input)
        elif check_user(user_input) == "username":
            username = user_input
        else:
            data = {
                "status": False,
                "message": "Siz kiritgan malumotlarga mos user topilmadi boshqattan kiriting",
            }
            raise ValidationError(data)

        auth_kwargs = {self.username_field: username, "password": password}
        user = authenticate(
            **auth_kwargs
        )  ### in the place, when username and password is given,
        ### the authenticate returns None or username us if there is user into.
        if user:
            self.user = user
        else:
            # self.trying_count += 1
            data = {
                "status": False,
                "message": "Username or password is wrong !!!",
            }
            raise ValidationError(data)

        user_check = User.objects.get(username=username)
        if user_check.auth_status != "complate":
            data = {
                "status": False,
                "message": "Siz hali toliq royhatdan otmagansiz",
            }
            raise ValidationError(data)

    def auth_by_email(self, email):
        user = User.objects.get(email=email)
        if not user:
            data = {
                "status": False,
                "message": "Siz kiritgan emailga mos user topilmadi boshqattan kiriting",
            }
            raise ValidationError(data)
        return user.username

    def validate(self, data):
        self.auth_validate(data=data)
        data = self.user.token()
        data["full_name"] = self.user.get_full_name
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UpdateAccessTokenSerizlizer(TokenRefreshSerializer):
    def validate(self, data):
        data = super().validate(data)
        access_token_instance = tokens.AccessToken(data["access"])
        user_id = access_token_instance["user_id"]
        user = generics.get_object_or_404(User, user_id)
        models.update_last_login(None, user=user)
        return data
