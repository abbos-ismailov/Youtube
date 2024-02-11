from django.contrib import admin
from .models import (
    Channel,
    HashTag,
    Video,
    HistoryView,
    VideoLike,
    VideoComment,
    CommentLike,
)

# Register your models here.

admin.site.register(Channel)
admin.site.register(HashTag)


class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "uuid"]
    readonly_fields = ["view_count"]


class LikeAdmin(admin.ModelAdmin):
    list_display = ["user", "video", "dislike"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["video", "user", "parent"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["video", "user", "uuid", "parent"]


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "comment"]


class HistoryVideoAdmin(admin.ModelAdmin):
    list_display = ["user", "video"]


admin.site.register(VideoLike, LikeAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoComment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(HistoryView, HistoryVideoAdmin)
