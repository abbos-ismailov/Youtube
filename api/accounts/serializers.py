from rest_framework import serializers
from api.accounts.models import User
from django.core.validators import FileExtensionValidator
from api.base.utility import send_email, check_username
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


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
        print(
            instance,
            "------------------------------ This is instance -------------------",
        )
        print(
            validated_data,
            "------------------------------ This is validated data -------------------",
        )
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
