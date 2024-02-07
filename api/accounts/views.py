from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import SignupSerializer, PersonalDataSerializer
from .models import User
from datetime import datetime

# Create your views here.


class SignupApiView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class VerifyCodeApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get("code")
        self.check_code(user, code)
        data = {
            "status": True,
            "auth_status": user.auth_status,
            "access": user.token()["access"],
            "refresh": user.token()["refresh"],
        }
        return Response(data=data)

    @staticmethod
    def check_code(user, code):
        verify_code = user.verify_code.filter(
            code_lifetime__gte=datetime.now(), is_confirmed=False, code=code
        )
        if not verify_code.exists():
            data = {
                "status": False,
                "message": "sizning parolingiz muddati tugagan yo xato",
            }

            raise ValidationError(data)
        else:
            verify_code.update(is_confirmed=True)
        if user.auth_status == "sent_email":
            user.auth_status = "verify_code"
            user.save()
        return True


class PersonalDataApiView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PersonalDataSerializer
    http_method_names = ["put", "patch"]

    def get_object(self):
        return self.request.user
    

    def update(self, request, *args, **kwargs):
        super(PersonalDataApiView, self).update(request, *args, **kwargs)
        data = {
            "status": True,
            "message": "Ro'yhatdan o'tdingiz",
            "auth_status": self.request.user.auth_status
        }
        return Response(data=data)
    
    def partial_update(self, request, *args, **kwargs):
        super(PersonalDataApiView, self).partial_update(request, *args, **kwargs)
        data = {
            "status": True,
            "message": "Ro'yhatdan o'tdingiz",
            "auth_status": self.request.user.auth_status
        }
        return Response(data=data)