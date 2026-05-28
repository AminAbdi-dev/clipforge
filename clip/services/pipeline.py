import os
import shutil
import uuid

from clip.services.youtube_utils import extract_video_id
from clip.models import ProcessedVideo

from clip.services.youtube import download_video
from clip.services.transcriber import transcribe_audio
from clip.services.hook_detector import detect_hooks
from clip.services.clipper import extract_clip
from clip.services.clip_subtitles import generate_clip_srt
from clip.services.burn_subtitles import burn_subtitles


def process_video(youtube_url):

    video_id = extract_video_id(youtube_url)

    print("VIDEO ID:", video_id)

    existing_video = ProcessedVideo.objects.filter(
        video_id=video_id
    ).first()

    existing_video = ProcessedVideo.objects.filter(
        video_id=video_id
    ).first()

    # CACHE HIT
    if (
        existing_video
        and os.path.exists(
            existing_video.video_path
        )
    ):

        print("USING CACHED VIDEO")

        video_path = existing_video.video_path

        transcript_segments = (
            existing_video.transcript_segments
        )

        title = existing_video.title

    # NEW VIDEO
    else:

        print("PROCESSING NEW VIDEO")

        # DOWNLOAD
        video_result = download_video(
            youtube_url
        )

        video_path = video_result[
            "video_path"
        ]

        title = video_result[
            "title"
        ]

        # TRANSCRIBE
        transcript_result = transcribe_audio(
            video_path
        )

        transcript_segments = (
            transcript_result["segments"]
        )

        # SAVE SOURCE DATA
        ProcessedVideo.objects.create(
            video_id=video_id,
            youtube_url=youtube_url,
            title=title,
            video_path=video_path,
            transcript_segments=transcript_segments,
        )

    # DETECT HOOKS
    hooks = detect_hooks(
        transcript_segments
    )

    if not hooks:
        return {
            "success": False,
            "message": "No hooks found"
        }

    best_hook = hooks[0]

    # EXTRACT CLIP
    clip_path = extract_clip(
        video_path=video_path,
        start=best_hook["start"],
        end=best_hook["end"],
        output_name=f"{uuid.uuid4()}.mp4"
    )

    # GENERATE SUBTITLE
    clip_srt = generate_clip_srt(
        segments=transcript_segments,
        clip_start=best_hook["start"],
        clip_end=best_hook["end"],
    )

    shutil.copy(
        clip_srt,
        "media/clips/clip_subtitles.srt"
    )

    print(
        "COPIED EXISTS:",
        os.path.exists(
            "media/clips/clip_subtitles.srt"
        )
    )

    # BURN SUBTITLE
    final_video = burn_subtitles(
        video_path=clip_path,
        subtitle_path=clip_srt,
        output_name=f"final_{uuid.uuid4()}.mp4"
    )

    return {
        "success": True,
        "cached": bool(existing_video),
        "title": title,
        "final_video": final_video.replace(
            "media\\",
            "/media/"
        ).replace(
            "\\",
            "/"
        ),
    }