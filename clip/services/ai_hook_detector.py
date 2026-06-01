import os
import json

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
)

load_dotenv()

endpoint = "https://models.github.ai/inference"

print("TOKEN:", os.getenv("GITHUB_TOKEN"))

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(
        os.getenv("GITHUB_TOKEN")
    ),
)


def detect_hooks_ai(segments):

    transcript = "\n".join(
        [
            f"{s['start']}|{s['end']}|{s['text']}"
            for s in segments[:100]
        ]
    )

    prompt = f"""
Find the 10 most viral clips.

Prefer clips between 10 and 30 seconds.

If the video is short, return the best available clips.

Never return an empty list.

Return ONLY JSON.

Format:

[
  {{
    "start": 0,
    "end": 5,
    "viral_score": 95
  }}
]

Transcript:

{transcript}
"""

    response = client.complete(
        messages=[
            SystemMessage(
                content="Return only JSON."
            ),
            UserMessage(
                content=prompt
            ),
        ],
        model="openai/gpt-4.1-mini"
    )

    content = response.choices[0].message.content

    print(content)

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    return json.loads(content)