import re


def clean_resume_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    text = text.replace("SKILLS", "Skills")
    text = text.replace("EDUCATION", "Education")
    text = text.replace("EXPERIENCE", "Experience")

    text = text.replace("•", "-")

    text = re.sub(
        r"[^a-zA-Z0-9.,:@+()/\- ]",
        "",
        text
    )

    return text.strip()