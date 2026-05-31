import os
import shutil
import uuid

from clip.services.ai_hook_detector import detect_hooks_ai
from clip.services.youtube_utils import extract_video_id
from clip.models import ProcessedVideo

from clip.services.youtube import download_video
from clip.services.transcriber import transcribe_audio
from clip.services.hook_detector import detect_hooks
from clip.services.clipper import extract_clip
from clip.services.clip_subtitles import generate_clip_srt
from clip.services.burn_subtitles import burn_subtitles


from clip.models import (
    ProcessedVideo,
    GeneratedShort
)

def process_video(
    youtube_url,
    short_count=1,
    user=None
):

    video_id = extract_video_id(youtube_url)

    print("VIDEO ID:", video_id)

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
        print("USING CACHED TRANSCRIPT")

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

    try:

        print("USING AI HOOK DETECTOR")

        hooks = detect_hooks_ai(
            transcript_segments
        )

        if not hooks:

            print("AI RETURNED NO HOOKS")

            hooks = detect_hooks(
                transcript_segments
            )

    except Exception as e:

        print("AI FAILED:", e)

        print("USING REGEX FALLBACK")

        hooks = detect_hooks(
            transcript_segments
        )

    print("HOOKS FOUND:", len(hooks))
    print(hooks)




    if not hooks:
        return {
            "success": False,
            "message": "No hooks found"
        }

    selected_hooks = hooks[:short_count]

    final_videos = []

    for hook in selected_hooks:

        clip_path = extract_clip(
            video_path=video_path,
            start=hook["start"],
            end=hook["end"],
        )

        clip_srt = generate_clip_srt(
            segments=transcript_segments,
            clip_start=hook["start"],
            clip_end=hook["end"],
        )

        shutil.copy(
            clip_srt,
            "media/clips/clip_subtitles.srt"
        )

        final_video = burn_subtitles(
            video_path=clip_path,
            subtitle_path=clip_srt,
            output_name=f"final_{uuid.uuid4()}.mp4"
        )

        final_videos.append(
            final_video.split("media")[-1].replace("\\", "/")
        )
        GeneratedShort.objects.create(
            user=user,
            title=title,
            youtube_url=youtube_url,
            final_video=final_video,
        )
    return {
        "success": True,
        "cached": bool(existing_video),
        "title": title,
        "videos": final_videos,
}

