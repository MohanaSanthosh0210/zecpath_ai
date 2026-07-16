# transcripts/transcript_cleaner.py

import re

FILLER_WORDS = [
    "um",
    "uh",
    "hmm",
    "like",
    "you know",
    "actually",
    "basically",
]


def clean_transcript(text):
    if not isinstance(text, str):
        return ""

    cleaned = text.lower()

    for word in FILLER_WORDS:
        cleaned = re.sub(rf"\b{word}\b", " ", cleaned)

    cleaned = re.sub(r"\[.*?\]", " ", cleaned)
    cleaned = re.sub(r"[^a-z0-9\s.,;:!?'-]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\b(\w+)\s+\1\b", r"\1", cleaned)

    return cleaned.strip()