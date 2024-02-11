from django.shortcuts import render, get_object_or_404
from .models import Video
from rest_framework import generics, views
from .serializers import VideoSerializer
from api.accounts.models import User
from api.base.custom_pagination import CustomPaginator
from rest_framework import permissions, response, status

# Create your views here.


class VideoListApiView(generics.ListAPIView):
    queryset = Video.objects.all()
    pagination_class = CustomPaginator
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.AllowAny,
    ]


class VideoCreateApiView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    def post(self, request):
        request.data["author"] = request.user.id
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data_response = {"status": True, "data": data}
            return response.Response(data_response, status=status.HTTP_201_CREATED)
        


