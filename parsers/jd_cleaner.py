import re


def clean_jd_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    text = text.replace(
        "REQUIRED SKILLS",
        "Required Skills"
    )

    text = re.sub(
        r"[^a-zA-Z0-9.,:@+()/\- ]",
        "",
        text
    )

    return text.strip()