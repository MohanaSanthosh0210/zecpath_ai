import json
import os
import re
from typing import Dict, List

INPUT_FOLDER = "data/sectioned_resumes"
OUTPUT_FOLDER = "data/academic_profiles"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

DEGREE_NORMALIZATION = [
    (r"\b(master(?:'s|s)?(?: degree| of science| of arts)?|m\.s\.c?|m\.?tech|mba)\b", "Master's Degree"),
    (r"\b(bachelor(?:'s|s)?(?: degree| of science| of arts)?|b\.s\.c?|b\.?tech)\b", "Bachelor's Degree"),
    (r"\b(associate(?:s)?(?:'s)? degree)\b", "Associate Degree"),
    (r"\b(graduate certificate|certificate in|certificate)\b", "Certificate"),
    (r"\b(ph\.d|doctorate)\b", "Doctorate"),
    (r"\b(diploma)\b", "Diploma")
]

FIELD_NORMALIZATION = [
    ("human computer interaction", "Human Computer Interaction"),
    ("interaction design", "Interaction Design"),
    ("information technology", "Information Technology"),
    ("computer science", "Computer Science"),
    ("food sciences", "Food Sciences"),
    ("nutrition", "Nutrition"),
    ("logistics and supply chain", "Logistics and Supply Chain"),
    ("supply chain", "Supply Chain"),
    ("warehousing", "Warehousing"),
    ("dietary education", "Dietary Education"),
    ("healthcare", "Healthcare"),
    ("public health", "Public Health"),
    ("business administration", "Business Administration")
]

CERTIFICATION_CATEGORY_KEYWORDS = {
    "Healthcare": [
        "nutrition",
        "diet",
        "health",
        "medical",
        "clinical",
        "dietitian"
    ],
    "Operations": [
        "warehousing",
        "supply chain",
        "logistics",
        "operations",
        "distribution"
    ],
    "Technical": [
        "computer",
        "software",
        "data",
        "analytics",
        "cloud",
        "machine learning",
        "ai",
        "cyber",
        "network",
        "engineering"
    ],
    "Compliance": [
        "safety",
        "osha",
        "regulatory",
        "compliance",
        "food safety",
        "licensed",
        "license"
    ],
    "Academic": [
        "graduate certificate",
        "certificate",
        "diploma",
        "course",
        "training"
    ],
    "Professional": [
        "professional",
        "project management",
        "pmp",
        "agile",
        "scrum",
        "consultant",
        "certified"
    ]
}

DEGREE_SEGMENT_PATTERN = re.compile(
    r"\b(?:Associates? Degree|Bachelor(?:'s)?(?: of)?|Bachelors? Degree|Master(?:'s)?(?: of)?|Masters? Degree|Graduate Certificate|Certificate in|Doctorate|Ph\.d|MBA|M\.S|M\.Tech|B\.Tech|BSc|MSc)\b",
    flags=re.I
)

INSTITUTION_PATTERN = re.compile(
    r"\b([A-Z][A-Za-z0-9&\.\-\s\(\)']{3,}?(?:University|College|Institute|School|Academy|Council|Center|Centre))\b",
    flags=re.I
)

DATE_SEPARATOR_PATTERN = re.compile(
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b",
    flags=re.I
)

DATE_PATTERN = re.compile(r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:\s+\d{4})?", flags=re.I)

ACHIEVEMENT_MARKERS = re.compile(r"\b(?:ACCOMPLISHMENTS|ACHIEVEMENTS|AWARDS)\b", flags=re.I)


def clean_text(value: str) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def normalize_degree_type(text: str) -> str:
    text = clean_text(text).lower()
    for pattern, normalized in DEGREE_NORMALIZATION:
        if re.search(pattern, text):
            return normalized
    return ""


def normalize_field_of_study(text: str) -> str:
    raw = clean_text(text)
    lower_text = raw.lower()
    for fragment, normalized in FIELD_NORMALIZATION:
        if fragment in lower_text:
            return normalized
    match = re.search(
        r"\b(?:in|major(?:s)?|concentration in|specialization in|focus(?:ed)? on)\s+([A-Za-z0-9&\-/() ]+?)(?:,|;|\.|$)",
        raw,
        flags=re.I,
    )
    if match:
        return match.group(1).strip(" ,;.-")
    return ""


def extract_graduation_year(text: str) -> str:
    years = re.findall(r"(?:19|20)\d{2}", clean_text(text))
    return str(max(map(int, years))) if years else ""


def split_education_sections(raw_text: str) -> List[str]:
    text = clean_text(raw_text)
    matches = list(DEGREE_SEGMENT_PATTERN.finditer(text))
    if len(matches) <= 1:
        return [text] if text else []
    starts = [match.start() for match in matches]
    if starts and starts[0] > 0:
        starts[0] = 0
    segments: List[str] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        segment = text[start:end].strip(" ,;.-")
        if segment:
            segments.append(segment)
    return segments


def extract_institution(text: str) -> str:
    cleaned = clean_text(text)
    institutions = INSTITUTION_PATTERN.findall(cleaned)
    if institutions:
        return institutions[-1].strip(" ,;.-")
    for part in re.split(r"[\n,;]\s*", cleaned):
        if any(keyword in part.lower() for keyword in ["university", "college", "institute", "school", "academy", "council", "center", "centre"]):
            return part.strip(" ,;.-")
    return ""


def categorize_certification(text: str) -> str:
    normalized = clean_text(text).lower()
    for category, keywords in CERTIFICATION_CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Other"


def extract_certification_names(raw_text: str) -> List[Dict[str, str]]:
    text = clean_text(raw_text)
    text = ACHIEVEMENT_MARKERS.split(text)[0]
    segments = DATE_SEPARATOR_PATTERN.split(text)
    certifications: List[str] = []
    for segment in segments:
        item = DATE_PATTERN.sub("", segment).strip(" ,;.-")
        if not item:
            continue
        if re.search(r"\b(?:certif|certificate|certified|course|training|license|licensed|graduate certificate|diploma)\b", item, flags=re.I):
            certifications.append(item)
    if not certifications and text:
        cleaned = DATE_PATTERN.sub("", text).strip(" ,;.-")
        if cleaned:
            certifications.append(cleaned)
    return [
        {
            "name": cert,
            "normalized_name": cert,
            "category": categorize_certification(cert),
            "source": "certifications",
        }
        for cert in certifications
    ]


def extract_education_text(raw_text: str) -> Dict:
    raw_text = clean_text(raw_text)
    if not raw_text:
        return {
            "education_items": [],
            "certifications": [],
            "education": [],
        }

    education_entries: List[Dict[str, str]] = []
    for segment in split_education_sections(raw_text):
        education_entries.append({
            "degree_type": normalize_degree_type(segment),
            "field_of_study": normalize_field_of_study(segment),
            "institution": extract_institution(segment),
            "graduation_year": extract_graduation_year(segment),
            "raw_text": segment,
        })

    certification_entries = extract_certification_names(raw_text)
    return {
        "education_items": education_entries,
        "certifications": certification_entries,
        "education": education_entries,
    }


def extract_education(data) -> Dict:
    if isinstance(data, str):
        return extract_education_text(data)

    education_sections = data.get("education", [])
    certification_sections = data.get("certifications", [])
    education_entries: List[Dict[str, str]] = []
    for raw_section in education_sections:
        for segment in split_education_sections(raw_section):
            education_entries.append({
                "degree_type": normalize_degree_type(segment),
                "field_of_study": normalize_field_of_study(segment),
                "institution": extract_institution(segment),
                "graduation_year": extract_graduation_year(segment),
                "raw_text": segment,
            })
    certification_entries: List[Dict[str, str]] = []
    for raw_section in certification_sections:
        certification_entries.extend(extract_certification_names(raw_section))
    return {
        "education": education_entries,
        "certifications": certification_entries,
        "education_items": education_entries,
    }


class EducationParser:
    """Parser wrapper for resume education extraction."""

    def extract_education(self, resume_text: str) -> Dict:
        return extract_education(resume_text)


if __name__ == "__main__":
    for file_name in os.listdir(INPUT_FOLDER):
        if not file_name.endswith(".json"):
            continue
        file_path = os.path.join(INPUT_FOLDER, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        profile = extract_education(data)
        output_file = os.path.join(OUTPUT_FOLDER, file_name.replace(".json", "_academic.json"))
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(profile, out, indent=4)
        print(f"Processed: {file_name}")