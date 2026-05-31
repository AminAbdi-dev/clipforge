from django.contrib import admin

from .models import (
    ProcessedVideo,
    GeneratedShort
)


admin.site.register(
    ProcessedVideo
)

admin.site.register(
    GeneratedShort
)