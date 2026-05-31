from rest_framework.decorators import api_view
from rest_framework.response import Response
from clip.models import GeneratedShort
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from clip.services.pipeline import process_video




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def process_video_api(request):

    youtube_url = request.data.get(
        "youtube_url"
    )

    short_count = int(
        request.data.get(
            "short_count",
            1
        )
    )

    if not youtube_url:
        return Response({
            "success": False,
            "message": "youtube_url is required"
        })

    result = process_video(
        youtube_url,
        short_count,
        request.user
    )

    return Response(result)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history_api(request):

    shorts = GeneratedShort.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )
    data = []

    for short in shorts:

        data.append({
            "title": short.title,
            "youtube_url": short.youtube_url,
            "final_video": short.final_video.split(
                "media"
            )[-1].replace(
                "\\",
                "/"
            ),
            "created_at": short.created_at,
        })

    return Response(data)





@api_view(["POST"])
def register_api(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:

        return Response({
            "success": False,
            "message": "username and password required"
        })

    if User.objects.filter(
        username=username
    ).exists():

        return Response({
            "success": False,
            "message": "username already exists"
        })

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "success": True,
        "user_id": user.id
    })


@api_view(["POST"])
def login_api(request):

    username = request.data.get(
        "username"
    )

    password = request.data.get(
        "password"
    )

    user = authenticate(
        username=username,
        password=password
    )

    if not user:

        return Response({
            "success": False,
            "message": "Invalid credentials"
        })

    refresh = RefreshToken.for_user(
        user
    )

    return Response({
        "success": True,
        "access": str(
            refresh.access_token
        ),
        "refresh": str(
            refresh
        ),
    })