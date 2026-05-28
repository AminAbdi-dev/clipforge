from django.urls import path

from clip.views import process_video_api


urlpatterns = [
    path(
        "process/",
        process_video_api
    ),
]