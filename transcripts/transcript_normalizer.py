"""
Day 24 – Transcript Normalization Module
"""

import re


def normalize_case(text):
    """
    Normalize casing.
    """

    text = text.lower()

    return text


def normalize_punctuation(text):
    """
    Add punctuation if missing.
    """

    text = text.strip()

    if text and text[-1] not in ".!?":
        text += "."

    return text


def normalize_transcript(text):
    """
    Full normalization pipeline.
    """

    text = normalize_case(text)

    text = re.sub(r"\s+", " ", text)

    text = normalize_punctuation(text)

    return text