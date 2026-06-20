"""
Day 24 – Speech-to-Text Integration & Cleaning

Deliverable:
Clean Transcript Processor
"""

import re


FILLER_WORDS = [
    "um",
    "uh",
    "erm",
    "ah",
    "like",
    "you know",
    "actually",
    "basically",
    "sort of",
    "kind of",
    "i mean"
]


def remove_fillers(text):
    """
    Remove filler words.
    """

    for filler in FILLER_WORDS:

        pattern = rf"\b{re.escape(filler)}\b"

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    return text


def remove_repeated_words(text):
    """
    Handle interrupted speech.

    Example:
    I I I worked on Python

    becomes

    I worked on Python
    """

    return re.sub(
        r"\b(\w+)(\s+\1\b)+",
        r"\1",
        text,
        flags=re.IGNORECASE
    )


def remove_noise_tokens(text):
    """
    Remove noise indicators.
    """

    noise_tokens = [
        "[noise]",
        "[silence]",
        "[background noise]",
        "[inaudible]"
    ]

    for token in noise_tokens:
        text = text.replace(token, "")

    return text


def clean_transcript(text):
    """
    Main cleaning pipeline.
    """

    if not text:
        return ""

    text = remove_noise_tokens(text)

    text = remove_fillers(text)

    text = remove_repeated_words(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()