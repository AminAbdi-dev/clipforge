from django.db import models


class ProcessedVideo(models.Model):

    youtube_url = models.URLField(unique=True)

    title = models.CharField(max_length=500)

    video_path = models.CharField(max_length=1000)

    final_video_path = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title