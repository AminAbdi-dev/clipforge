import subprocess
from pathlib import Path
import shutil


def burn_subtitles(video_path, subtitle_path, output_name="final_auto_clip.mp4"):

    output_dir = Path("media/final")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = (output_dir / output_name).resolve()

    video_path = Path(video_path).resolve()

    temp_subtitle = Path("clip_subtitles.srt").resolve()

    shutil.copy(
        subtitle_path,
        temp_subtitle
    )

    command = (
        f'ffmpeg -y -i "{video_path}" '
        f'-vf subtitles=clip_subtitles.srt '
        f'"{output_path}"'
    )

    print("COMMAND:", command)

    subprocess.run(
        command,
        shell=True,
        check=True
    )

    print("VIDEO EXISTS:", output_path.exists())

    temp_subtitle.unlink(missing_ok=True)

    return str(output_path)