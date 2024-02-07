from django.urls import path
from .views import SignupApiView, VerifyCodeApiView, PersonalDataApiView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', SignupApiView.as_view()),
    path('verify-code/', VerifyCodeAp