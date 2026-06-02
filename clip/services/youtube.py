from yt_dlp import YoutubeDL
from pathlib import Path
import uuid
import os
import base64

MEDIA_ROOT = Path("media")
MEDIA_ROOT.mkdir(exist_ok=True)


def download_video(youtube_url: str):

    unique_id = str(uuid.uuid4())
    output_path = MEDIA_ROOT / f"{unique_id}.%(ext)s"

    # Create cookie file from Railway env variable
    cookie_file = Path("/tmp/youtube_cookies.txt")

    cookies_b64 = os.getenv("YOUTUBE_COOKIES_B64")

    if cookies_b64:
        cookie_file.write_bytes(
            base64.b64decode(cookies_b64)
        )

    print("COOKIE ENV EXISTS:", bool(os.getenv("YOUTUBE_COOKIES_B64")))
    print("COOKIE FILE EXISTS:", cookie_file.exists())
    print("COOKIE SIZE:", cookie_file.stat().st_size)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": str(output_path),
        "quiet": False,
        "noplaylist": True,
        "cookiefile": str(cookie_file),

        "source_address": "0.0.0.0",

        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            print("YTDLP VERSION TEST")
            info = ydl.extract_info(youtube_url, download=True)
        except Exception as e:
            print("YTDLP ERROR:", str(e))
            raise

    downloaded_file = MEDIA_ROOT / f"{unique_id}.mp4"

    return {
        "title": info.get("title"),
        "video_path": str(downloaded_file),
    }