from rest_framework import serializers
from .models import Video, VideoLike


class VideoSerializer(serializers.ModelSerializer):
    video_like_count = serializers.SerializerMethodField("get_video_like_count")
    video_comment_count = serializers.SerializerMethodField("get_video_comment_count")
    video_me_like = serializers.SerializerMethodField("get_video_me_like")

    class Meta:
        model = Video
        fields = (
            "uuid",
            "create_at",
            "title",
            "description",
            "author",
            "file",
            "video_like_count",
            "view_count",
            "video_comment_count",
            "video_me_like",
        )
        extra_kwargs = {"author": {"required": False}}

    @staticmethod
    def get_video_like_count(obj):
        return obj.video_videoLike.count()

    @staticmethod
    def get_video_comment_count(obj):
        return obj.video_videoComment.count()

    def get_video_me_like(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:
                like = VideoLike.objects.get(video=obj, user=request.user)
                if like.dislike:
                    return -1
                else:
                    return 1
            except VideoLike.DoesNotExist:
                return 0
        else:
            return 0
