from django.urls import path
from .views import VideoListApiView, VideoCreateApiView

urlpatterns = [
    path("", VideoListApiView.as_view()),
    path("video-create/", VideoCreateApiView.as_view()),
]