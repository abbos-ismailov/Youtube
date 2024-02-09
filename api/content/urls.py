from django.urls import path
from .views import VideoListApiView

urlpatterns = [
    path("", VideoListApiView.as_view()),
]