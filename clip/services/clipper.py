import subprocess
from pathlib import Path


OUTPUT_DIR = Path("media/clips")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_clip(video_path, start, end, output_name="clip.mp4"):

    output_path = OUTPUT_DIR / output_name

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
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        str(output_path),
    ]

    subprocess.run(command, check=True)

    return str(output_path)