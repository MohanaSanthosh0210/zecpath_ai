import re

def clean_resume_text(text):

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Normalize section headings
    text = text.replace("SKILLS", "Skills")
    text = text.replace("EDUCATION", "Education")
    text = text.replace("EXPERIENCE", "Experience")

    # Normalize bullet points
    text = text.replace("•", "-")

    # Remove unwanted symbols
    text = re.sub(r"[^a-zA-Z0-9.,:@+()/ -]", "", text)

    return text.strip()