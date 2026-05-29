import re

def clean_jd_text(text):

    text = re.sub(r"\s+", " ", text)

    text = text.replace("REQUIRED SKILLS", "Required Skills")

    text = text.strip()

    return text