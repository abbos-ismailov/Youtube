# Generated by Django 5.0.1 on 2024-02-09 18:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_commentLike', to='content.videocomment'),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_commentLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historyview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_historyView', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historyview',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_historyView', to='content.video'),
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_videoComment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_videoComment', to='content.video'),
        ),
        migrations.AlterField(
            model_name='videolike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_videoLike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='videolike',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_videoLike', to='content.video'),
        ),
    ]