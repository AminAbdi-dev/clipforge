from django.db import models


class ProcessedVideo(models.Model):

    youtube_url = models.URLField()

    video_id = models.CharField(
        max_length=100,
        unique=True
    )

    title = models.CharField(
        max_length=500
    )

    video_path = models.CharField(
        max_length=1000
    )

    transcript_segments = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )