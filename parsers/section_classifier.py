import re

SECTION_HEADERS = {
    "profile": [
        "profile",
        "summary",
        "objective",
        "professional summary",
        "career objective"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "professional skills"
    ],

    "experience": [
        "experience",
        "work experience",
        "employment history",
        "professional experience",
        "employment"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications"
    ],

    "certifications": [
        "certifications",
        "licenses",
        "courses",
        "training"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects"
    ]
}


def clean_heading(text):
    """
    Normalize heading text.
    """
    text = text.strip().lower()

    text = re.sub(r'[:\-]+$', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text


def detect_sections(text):

    original_text = text.replace("\r", " ").replace("\n", " ")
    normalized_text = re.sub(r"\s+", " ", original_text).strip()

    matches = []

    for section, keywords in SECTION_HEADERS.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            for match in re.finditer(pattern, normalized_text, flags=re.IGNORECASE):
                actual_text = normalized_text[match.start():match.end()]
                if actual_text.isupper() or actual_text.istitle():
                    matches.append((match.start(), match.end(), section))

    if not matches:
        return {"other": [text.strip()]}

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))

    filtered_matches = []
    for start, end, section in matches:
        if filtered_matches and start < filtered_matches[-1][1]:
            continue
        filtered_matches.append((start, end, section))

    sections = {}

    for index, (start, end, section) in enumerate(filtered_matches):
        section_start = end
        section_end = filtered_matches[index + 1][0] if index + 1 < len(filtered_matches) else len(normalized_text)
        section_text = normalized_text[section_start:section_end].strip()

        if not section_text:
            continue

        if section not in sections:
            sections[section] = []

        sections[section].append(section_text)

    first_heading_start = matches[0][0]
    if first_heading_start > 0:
        leading_text = normalized_text[:first_heading_start].strip()
        if leading_text:
            sections.setdefault("other", []).append(leading_text)

    return sections