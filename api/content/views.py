from django.shortcuts import render
from .models import Video
from rest_framework import generics
from .serializers import VideoSerializer
from api.base.custom_pagination import CustomPaginator
from rest_framework import permissions
# Create your views here.

class VideoListApiView(generics.ListAPIView):
    queryset = Video.objects.all()
    pagination_class = CustomPaginator
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny, ] 