from django.db import models
from api.base.models import BaseContentModel
from api.accounts.models import User
# Create your models here.

class Channel(BaseContentModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    banner = models.ImageField(upload_to="channel-banner/", null=True, blank=True)
    avatar = models.ImageField(upload_to="user-avatars/", null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_channel"
    )
    follower = models.ManyToManyField(User, related_name="user_follower")

    def __str__(self) -> str:
        return self.name


class HashTag(BaseContentModel):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Video(BaseContentModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_video"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to="Video/")
    tags = models.ManyToManyField(HashTag, related_name="hashtag_video")
    view_count = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

class HistoryView(BaseContentModel): 
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_history_view"
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="video_history_view"
    )

    def __str__(self) -> str:
        return self.user.username

class VideoLike(BaseContentModel):  
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_video_like"
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="video_video_like"
    )
    dislike = models.BooleanField(default=False) ### in default situation, it isn't created. if user clicks like, it will be created

    def __str__(self) -> str:
        return f"{self.user.username} dislike={self.dislike}"

class VideoComment(BaseContentModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_video_comment"
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="video_video_comment"
    )
    comment = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="comment_children"
    )

    def __str__(self) -> str:
        return f"{self.user.username} {self.video.title}"

class CommentLike(BaseContentModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment_like"
    )
    comment = models.ForeignKey(
        VideoComment, on_delete=models.CASCADE, related_name="video_comment_like"
    )

    def __str__(self) -> str:
        return f"{self.user.username} {self.comment.video.title}"