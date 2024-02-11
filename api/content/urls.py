from django.urls import path
from .views import VideoListApiView, VideoRetriwApiView, VideoCreateApiView, PutDeleteVideoApiView, LikeCreateApiView, CommentCreateApiView

urlpatterns = [
    path("", VideoListApiView.as_view()),
    path("<uuid:uuid>/", VideoRetriwApiView.as_view()),
    path("video-post/", VideoCreateApiView.as_view()),
    path("video-put/<uuid:uuid>", PutDeleteVideoApiView.as_view()),
    path("like-post/", LikeCreateApiView.as_view()),
    path("comment-post/", CommentCreateApiView.as_view()),
]