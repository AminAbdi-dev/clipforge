from yt_dlp import YoutubeDL
from pathlib import Path
import uuid


MEDIA_ROOT = Path("media")
MEDIA_ROOT.mkdir(exist_ok=True)


def download_video(youtube_url: str):

    unique_id = str(uuid.uuid4())

    output_path = MEDIA_ROOT / f"{unique_id}.%(ext)s"

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": str(output_path),
        "quiet": False,
        "noplaylist": True,
        "impersonate": "chrome",

        "extractor_args": {
            "youtube": {
                "player_client": [
                    "android",
                    "ios"
                ]
            }
        }
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)

    downloaded_file = MEDIA_ROOT / f"{unique_id}.mp4"

    return {
        "title": info.get("title"),
        "video_path": str(downloaded_file),
    }