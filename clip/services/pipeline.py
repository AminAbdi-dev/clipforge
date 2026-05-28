import os
import shutil

from clip.models import ProcessedVideo

from clip.services.youtube import download_video
from clip.services.transcriber import transcribe_audio
from clip.services.hook_detector import detect_hooks
from clip.services.clipper import extract_clip
from clip.services.clip_subtitles import generate_clip_srt
from clip.services.burn_subtitles import burn_subtitles


def process_video(youtube_url):

    # CHECK CACHE
    existing_video = ProcessedVideo.objects.filter(
        youtube_url=youtube_url
    ).first()

    if existing_video:

        print("USING CACHED VIDEO")

        return {
            "success": True,
            "cached": True,
            "title": existing_video.title,
            "final_video": existing_video.final_video_path,
        }

    print("PROCESSING NEW VIDEO")

    # DOWNLOAD
    video_result = download_video(youtube_url)

    # TRANSCRIBE
    transcript_result = transcribe_audio(
        video_result["video_path"]
    )

    # DETECT HOOKS
    hooks = detect_hooks(
        transcript_result["segments"]
    )

    if not hooks:
        return {
            "success": False,
            "message": "No hooks found"
        }

    best_hook = hooks[0]

    # EXTRACT CLIP
    clip_path = extract_clip(
        video_path=video_result["video_path"],
        start=best_hook["start"],
        end=best_hook["end"],
        output_name="auto_clip.mp4"
    )

    # GENERATE CLIP SUBTITLE
    clip_srt = generate_clip_srt(
        segments=transcript_result["segments"],
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



    print("CLIP SRT PATH:", clip_srt)

    print(
        "FILE EXISTS:",
        os.path.exists(clip_srt)
    )



    # BURN SUBTITLE
    final_video = burn_subtitles(
        video_path=clip_path,
        subtitle_path=clip_srt,
        output_name="final_auto_clip.mp4"
    )

    # SAVE TO DATABASE
    ProcessedVideo.objects.create(
        youtube_url=youtube_url,
        title=video_result["title"],
        video_path=video_result["video_path"],
        final_video_path=final_video,
    )

    return {
        "success": True,
        "cached": False,
        "title": video_result["title"],
        "final_video": final_video,
    }