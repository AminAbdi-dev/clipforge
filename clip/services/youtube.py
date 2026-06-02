from yt_dlp import YoutubeDL
from pathlib import Path
from yt_dlp.utils import DownloadError
import uuid
import os
import base64



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
        "cookiefile": str(cookie_file),
        
        "extractor_args": {
            "youtube": {
                "player_client": [
                    "android",
                    "ios"
                ]
            }
        },

        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }
    }
    print("COOKIE FILE EXISTS:", Path("cookies/cookies.txt").exists())

    cookie_file = Path("/tmp/youtube_cookies.txt")

    if not cookie_file.exists():
        cookies_b64 = os.getenv("YOUTUBE_COOKIES_B64")

        if cookies_b64:
            cookie_file.write_bytes(
                base64.b64decode(cookies_b64)
            )
    
    print("COOKIE ENV EXISTS:", bool(os.getenv("YOUTUBE_COOKIES_B64")))
    print("COOKIE FILE EXISTS:", cookie_file.exists())
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=True)
        except Exception as e:
            print("YTDLP ERROR:", str(e))
            raise

    downloaded_file = MEDIA_ROOT / f"{unique_id}.mp4"

    return {
        "title": info.get("title"),
        "video_path": str(downloaded_file),
    }

    