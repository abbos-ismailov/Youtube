from django.contrib import admin
from .models import Channel, HashTag, Video, HistoryView, VideoLike, VideoComment, CommentLike
# Register your models here.

admin.site.register(Channel)
admin.site.register(HashTag)
admin.site.register(Video)
admin.site.register(HistoryView)
admin.site.register(VideoLike)
admin.site.register(VideoComment)
admin.site.register(CommentLike)