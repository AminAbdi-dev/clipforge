from rest_framework.decorators import api_view
from rest_framework.response import Response

from clip.services.pipeline import process_video


@api_view(["POST"])
def process_video_api(request):

    youtube_url = request.data.get(
        "youtube_url"
    )

    if not youtube_url:
        return Response({
            "success": False,
            "message": "youtube_url is required"
        })

    result = process_video(
        youtube_url
    )

    return Response(result)