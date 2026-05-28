from urllib.parse import urlparse, parse_qs


def extract_video_id(url):

    parsed = urlparse(url)

    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")

    query = parse_qs(parsed.query)

    return query.get("v", [None])[0]