def format_timestamp(seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def generate_clip_srt(
    segments,
    clip_start,
    clip_end,
    output_file="media/clip_subtitles.srt"
):

    output_path = output_file

    filtered_segments = []

    for segment in segments:

        seg_start = segment["start"]
        seg_end = segment["end"]

        if seg_end >= clip_start and seg_start <= clip_end:

            adjusted_start = max(0, seg_start - clip_start)
            adjusted_end = max(0, seg_end - clip_start)

            filtered_segments.append({
                "start": adjusted_start,
                "end": adjusted_end,
                "text": segment["text"]
            })
            print(segment["text"])

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        for idx, segment in enumerate(filtered_segments, start=1):

            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])

            f.write(f"{idx}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment['text'].strip()}\n\n")

    return output_file