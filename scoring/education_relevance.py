import re
from typing import Optional

FIELD_GROUPS = [
    {
        "computer science",
        "software engineering",
        "information technology",
        "human computer interaction",
        "computer engineering",
        "data science",
        "cybersecurity",
    },
    {"logistics", "supply chain", "operations", "warehousing", "distribution"},
    {"nutrition", "food sciences", "dietary education", "healthcare", "public health"},
    {"business", "business administration", "management", "marketing", "finance"},
]

DEGREE_LEVEL_MAP = {
    "doctorate": 5,
    "phd": 5,
    "master": 4,
    "mba": 4,
    "mtech": 4,
    "msc": 4,
    "bachelor": 3,
    "btech": 3,
    "bsc": 3,
    "associate": 2,
    "certificate": 1,
    "graduate certificate": 1,
    "diploma": 1,
    "course": 1,
}


def normalize_field(field: str) -> str:
    if not field:
        return ""
    value = field.lower().strip()
    return re.sub(r"[^a-z0-9\s]", "", value)


def degree_level(degree: Optional[str]) -> int:
    if not degree:
        return 0
    text = normalize_field(degree)
    for key, level in DEGREE_LEVEL_MAP.items():
        if key in text:
            return level
    return 0


def fields_are_related(candidate_field: str, required_field: str) -> bool:
    candidate = normalize_field(candidate_field)
    required = normalize_field(required_field)
    if not candidate or not required:
        return False
    if candidate == required:
        return True
    for group in FIELD_GROUPS:
        if candidate in group and required in group:
            return True
    return False


def calculate_education_score(
    candidate_field: str,
    required_field: str,
    candidate_degree: Optional[str] = None,
    required_degree: Optional[str] = None,
) -> int:
    candidate_field_norm = normalize_field(candidate_field)
    required_field_norm = normalize_field(required_field)

    if not candidate_field_norm or not required_field_norm:
        return 0

    if candidate_field_norm == required_field_norm:
        score = 100
    elif fields_are_related(candidate_field, required_field):
        score = 80
    elif candidate_field_norm in required_field_norm or required_field_norm in candidate_field_norm:
        score = 70
    else:
        score = 50

    if candidate_degree and required_degree:
        candidate_level = degree_level(candidate_degree)
        required_level = degree_level(required_degree)
        if candidate_level and required_level:
            if candidate_level == required_level:
                score = min(100, score + 10)
            elif candidate_level > required_level:
                score = min(100, score + 5)
            else:
                score = max(0, score - 5)

    return score