# transcripts/transcript_cleaner.py

import re

FILLER_WORDS = [
    "um",
    "uh",
    "hmm",
    "like",
    "you know",
    "actually",
    "basically"
]


def clean_transcript(text):

    text = text.lower()

    for word in FILLER_WORDS:

        text = re.sub(
            rf"\b{word}\b",
            "",
            text
        )

    text = re.sub(
        r"\[.*?\]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = re.sub(
        r"\b(\w+)\s+\1\b",
        r"\1",
        text
    )

    return text.strip()