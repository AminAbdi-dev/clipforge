import re


VIRAL_PATTERNS = [
    r"\b(secret|truth|nobody knows|they lied|warning)\b",
    r"\b(crazy|insane|unbelievable|shocking)\b",
    r"\b(million|billion|money|rich)\b",
    r"\b(ai|future|robot|technology)\b",
    r"\b(danger|risk|destroy|death|survive)\b",
    r"\b(mistake|problem|failed|failure)\b",
]


def calculate_score(text):

    score = 0

    text_lower = text.lower()

    for pattern in VIRAL_PATTERNS:
        if re.search(pattern, text_lower):
            score += 20

    if "?" in text:
        score += 10

    if len(text.split()) >= 12:
        score += 5

    if any(word in text_lower for word in [
        "but",
        "however",
        "suddenly",
        "unexpectedly",
        "fortunately",
    ]):
        score += 10

    return score


def detect_hooks(segments):

    clips = []

    for segment in segments:

        score = calculate_score(segment["text"])

        if score >= 20:

            clips.append({
                "start": round(segment["start"], 2),
                "end": round(segment["end"], 2),
                "text": segment["text"],
                "viral_score": score,
            })

    clips = sorted(
        clips,
        key=lambda x: x["viral_score"],
        reverse=True
    )

    return clips[:10]