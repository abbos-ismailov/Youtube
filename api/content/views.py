from django.shortcuts import render, get_object_or_404
from .models import Video, VideoLike, VideoComment
from rest_framework import generics, views, exceptions
from .serializers import (
    VideoSerializer,
    LikeSerializer,
    CommentSerializer,
)
from api.accounts.models import User
from api.base.custom_pagination import CustomPaginator
from rest_framework import permissions, response, status

# Create your views here.


############################### ------------  Video CRUD
class VideoListApiView(generics.ListAPIView):
    queryset = Video.objects.all()
    pagination_class = CustomPaginator
    serializer_class = VideoSerializer
    permission_classes = [
        permissions.AllowAny,
    ]


class VideoRetriwApiView(views.APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request, uuid):
        video = get_object_or_404(Video, uuid=uuid)
        serializer = VideoSerializer(video)
        # print(video.video_videoComment.all(), "---------------------------------")
        serializer_comment = CommentSerializer(video.video_videoComment.all(), many=True)
        data = {
            "status": True,
            "data": serializer.data,
            "comment": serializer_comment.data
        }
        return response.Response(data, status=status.HTTP_200_OK)


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


class PutDeleteVideoApiView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def put(self, request, uuid):
        video = get_object_or_404(Video, uuid=uuid)
        data = request.data
        serializer = VideoSerializer(data=data, instance=video, partial=True)

        if serializer.is_valid(raise_exception=True):
            if video.author.id == request.user.id:
                serializer.save()
                data = {"status": True, "message": f"Update your video --> {video}"}
                return response.Response(data=data)

    def delete(self, request, uuid):
        video = get_object_or_404(Video, uuid=uuid)
        if video.author.id == request.user.id:
            video.delete()
            data = {"status": True, "message": f"Delete your video --> {video}"}
            return response.Response(data=data)


##################################################### ------- Video CRUD Finished


#### Like started
class LikeCreateApiView(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = VideoLike.objects.all()
    serializer_class = LikeSerializer

    def post(self, request):
        request.data["user"] = request.user.id
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            check_click = VideoLike.objects.filter(user=request.user.id).first()
            if check_click:
                if check_click.dislike == data["dislike"]:
                    check_click.delete()
                    response_delete = {
                        "status": True,
                        "message": "userning avvalgi like yo dislike ochdi",
                    }
                    return response.Response(response_delete)
                else:
                    response_put = {
                        "status": True,
                        "message": "user avvalgi like Ozgardi",
                    }
                    if check_click.dislike:
                        check_click.dislike = False
                        response_put["message"] = "userning avvalgi dislike Ozgardi"
                    else:
                        check_click.dislike = True
                    check_click.save()
                    return response.Response(response_put)

            serializer.save()
            video = data.get("video")
            dislike = data.get("dislike")
            data = {
                "status": True,
                "message": f"Like bosildi bu videoga {video}",
            }
            if dislike:
                data["message"] = f"Dislike bosildi bu videoga --> {video}"

            return response.Response(data=data)


####### Like finished


####### Comment Started


class CommentCreateApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = VideoComment.objects.all()
    serializer_class = CommentSerializer
    def post(self, request):
        request.data["user"] = request.user.id
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "status": True,
                "message": "Comment Created"
            }
            return response.Response(data)
