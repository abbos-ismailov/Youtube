from django.urls import path
from .views import SignupApiView, VerifyCodeApiView, PersonalDataApiView, LoginApiView, LogoutApiView, UpdateAccessTokenApiView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', SignupApiView.as_view()),
    path('verify-code/', VerifyCodeApiView.as_view()),
    path('personal-data/', PersonalDataApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('update-access/', UpdateAccessTokenApiView.as_view()),
]



if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
