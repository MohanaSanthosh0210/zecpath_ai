# transcripts/transcript_normalizer.py

import re


def normalize_transcript(text):

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    if len(text) > 0:

        text = (
            text[0].upper() +
            text[1:]
        )

    if not text.endswith("."):

        text += "."

    return text