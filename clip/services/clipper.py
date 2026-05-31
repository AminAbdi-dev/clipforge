import subprocess
from pathlib import Path
import uuid


OUTPUT_DIR = Path("media/clips")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_clip(video_path, start, end):

    unique_name = f"{uuid.uuid4()}.mp4"

    output_path = OUTPUT_DIR / unique_name

    duration = end - start

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,

        "-ss",
        str(start),

        "-t",
        str(duration),

        "-vf",
        (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920"
        ),

        "-c:v",
        "libx264",

        "-c:a",
        "aac",

        str(output_path),
    ]

    subprocess.run(command, check=True)

    return str(output_path)