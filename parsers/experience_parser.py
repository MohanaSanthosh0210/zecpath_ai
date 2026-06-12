import json
import os
import re
import calendar
from datetime import date, datetime
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

from utils.logger import logger

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

TITLE_HINTS = [
    "engineer", "developer", "manager", "director", "lead", "architect", "analyst",
    "specialist", "consultant", "officer", "coordinator", "administrator", "supervisor",
    "scientist", "principal", "product", "project", "program"
]

SECTION_HEADING_PATTERN = re.compile(
    r"(?mi)(?:professional\s+experience|work\s+experience|employment\s+history|career\s+history|experience\s+summary)",
)

SECTION_BREAK_PATTERN = re.compile(
    r"(?mi)(?:education|skills|certifications|projects|summary|profile|awards|languages|interests|hobbies)",
)

DATE_RANGE_PATTERN = re.compile(
    r"(?P<start>(?:Q[1-4]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|\d{4}))"
    r"\s*(?:-|–|—|to|through|until)?\s*"
    r"(?P<end>(?:Q[1-4]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|\d{4}|Present|Current|Now))",
    re.IGNORECASE,
)

DATE_TOKEN_PATTERN = re.compile(
    r"(?:Q[1-4]\s*\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|\d{4}|Present|Current|Now)",
    re.IGNORECASE,
)

COMPANY_TITLE_SEPARATORS = re.compile(r"\s+(?:@|at|with|for)\s+", re.IGNORECASE)


class ExperienceParser:
    """Parse resume experience text into structured experience objects."""

    def __init__(self, gap_months_threshold: int = 2):
        self.gap_months_threshold = gap_months_threshold

    def extract_experience(self, resume_text: str) -> Dict:
        """
        Extract experience items and summary metrics from resume text.
        """

        try:
            if not resume_text:
                return {
                "experience_items": [],
                "total_experience_years": 0.0,
                "total_experience_months": 0,
                "gaps": [],
                "overlaps": [],
                "experience_summary": {},
            }

            normalized_text = self._normalize_text(
            resume_text
            )

            section_text = self._find_experience_section(
            normalized_text
            )

            entry_texts = self._split_entries(
            section_text or normalized_text
            )

            experience_items = []

            for entry_text in entry_texts:

                item = self._parse_experience_entry(
                entry_text
                )

                if item:
                    experience_items.append(item)

            merged = self._merge_duplicate_entries(
                experience_items
            )

            metrics = self._summarize_experience(
                merged
            )

            return {
                "experience_items": merged,
                "total_experience_years": round(
                    metrics["total_experience_years"],
                    2
                ),
                "total_experience_months":
                    metrics["total_experience_months"],
                "gaps": metrics["gaps"],
                "overlaps": metrics["overlaps"],
                "experience_summary": metrics,
        }

        except Exception as e:

            logger.error(
            f"Experience Parsing Failed: {str(e)}"
        )

            return {
            "experience_items": [],
            "total_experience_years": 0.0,
            "total_experience_months": 0,
            "gaps": [],
            "overlaps": [],
            "experience_summary": {},
        }

    def save_experience_json(self, experience_data: Dict, output_dir: str = "data/extracted_experience", filename: Optional[str] = None) -> str:
        """Save parsed experience output to a JSON file."""
        os.makedirs(output_dir, exist_ok=True)
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"experience_{timestamp}.json"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as outfile:
            json.dump(experience_data, outfile, indent=2, ensure_ascii=False)

        logger.info(f"Saved experience JSON to {filepath}")
        return filepath

    def _normalize_text(self, text: str) -> str:
        normalized = re.sub(r"\r\n|\r", "\n", text)
        normalized = re.sub(
            r"(?mi)(EMPLOYMENT HISTORY|PROFESSIONAL EXPERIENCE|WORK EXPERIENCE|CAREER HISTORY|EXPERIENCE SUMMARY)",
            r"\n\1\n",
            normalized,
        )
        normalized = re.sub(r"(?<=[:\n])\s*-\s+", "\n- ", normalized)
        normalized = re.sub(r"\n{2,}", "\n\n", normalized)
        return normalized.strip()

    def _find_experience_section(self, text: str) -> Optional[str]:
        match = SECTION_HEADING_PATTERN.search(text)
        if not match:
            return None

        start = match.end()
        next_break = SECTION_BREAK_PATTERN.search(text[start:])
        end = start + next_break.start() if next_break else len(text)

        return text[start:end].strip()

    def _split_entries(self, text: str) -> List[str]:
        entries = self._split_entries_by_date_ranges(text)
        if entries:
            return entries

        if not text:
            return []

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        entries = []
        current = []

        for line in lines:
            if self._is_heading_line(line):
                continue

            if line.startswith(("-", "*", "•")):
                if current:
                    entries.append("\n".join(current))
                current = [line.lstrip("-*• ").strip()]
            elif current and self._is_continuation_line(line):
                current.append(line)
            else:
                if current:
                    entries.append("\n".join(current))
                current = [line]

        if current:
            entries.append("\n".join(current))

        return entries

    def _split_entries_by_date_ranges(self, text: str) -> List[str]:
        if not text:
            return []

        matches = list(DATE_RANGE_PATTERN.finditer(text))
        if len(matches) < 1:
            return []

        entries = []
        for index, match in enumerate(matches):
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            entry_text = text[start:end].strip()
            if entry_text:
                entries.append(entry_text)

        return entries

    def _is_heading_line(self, line: str) -> bool:
        return bool(SECTION_HEADING_PATTERN.match(line))

    def _is_continuation_line(self, line: str) -> bool:
        return not DATE_RANGE_PATTERN.search(line)

    def _parse_experience_entry(self, entry_text: str) -> Optional[Dict]:
        entry_text = entry_text.strip()
        if not entry_text:
            return None

        dates = self._extract_date_range(entry_text)
        start_date, end_date, duration_text = self._parse_duration(dates) if dates else (None, None, None)

        content = self._remove_date_text(entry_text, dates) if dates else entry_text
        header_text = self._extract_header_text(content)
        company, designation, location = self._extract_company_and_designation(header_text)
        if not company and not designation:
            company, designation, location = self._guess_company_and_designation(header_text)

        responsibilities = self._extract_responsibilities(content)

        return {
            "company": company or "unknown",
            "designation": designation or "unknown",
            "location": location,
            "duration": duration_text or (dates or "unknown"),
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "duration_months": self._calculate_months(start_date, end_date) if start_date and end_date else None,
            "responsibilities": responsibilities,
            "raw_text": entry_text,
        }

    def _extract_company_and_designation(self, text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        text = text.strip()
        designation = None
        company = None
        location = None

        if "," in text:
            parts = [part.strip() for part in text.split(",") if part.strip()]
            designation = parts[0]
            company = " ".join(parts[1:]).strip()
        else:
            separator_match = COMPANY_TITLE_SEPARATORS.search(text)
            if separator_match:
                parts = COMPANY_TITLE_SEPARATORS.split(text, maxsplit=1)
                if len(parts) == 2:
                    if self._contains_title_hint(parts[0]):
                        designation = parts[0].strip()
                        company = parts[1].strip()
                    else:
                        company = parts[0].strip()
                        designation = parts[1].strip()

        if company:
            company = self._clean_company_name(company)
            company = self._strip_company_description(company)
            location = self._extract_location(company)
            if location:
                company = company.replace(location, "").strip(" ,")

        return company, designation, location

    def _clean_company_name(self, text: str) -> str:
        return re.sub(r"[|\-–—]+$", "", text).strip(" ,|-–—")

    def _clean_designation(self, text: str) -> str:
        return text.strip(" ,|-–—")

    def _strip_company_description(self, text: str) -> str:
        split = re.split(
            r"(?i)\b(?:is|provides|offers|delivers|serves|specializes|focuses|supports|powers|helps|is a|is an|is the)\b",
            text,
            maxsplit=1,
        )
        return split[0].strip(" ,")

    def _extract_location(self, text: str) -> Optional[str]:
        location_match = re.search(
            r"\b(?:New York|London|San Francisco|Los Angeles|Chicago|Boston|Seattle|Toronto|Vancouver|Austin|Berlin|Amsterdam|Sydney|Melbourne|Paris|Dublin)\b",
            text,
            re.IGNORECASE,
        )
        return location_match.group(0).strip() if location_match else None

    def _guess_company_and_designation(self, text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        lower = text.lower()
        if self._contains_title_hint(lower):
            return None, text.strip(), None

        if any(keyword in lower for keyword in ["inc", "llc", "corp", "company", "solutions", "technologies", "systems"]):
            return text.strip(), None, None

        return None, text.strip(), None

    def _extract_header_text(self, content: str) -> str:
        split = re.split(
            r"(?i)\b(?:As the|As a|As an|My core|My responsibilities|Responsibilities|Core activities included|Core responsibilities|Working closely with|As part of|In this role)\b",
            content,
            maxsplit=1,
        )
        return split[0].strip(" .,-")

    def _extract_responsibilities(self, content: str) -> List[str]:
        bullets = re.findall(r"-\s*([^\-\n]+)", content)
        responsibilities = [bullet.strip(" .") for bullet in bullets if bullet.strip()]
        if responsibilities:
            return responsibilities

        # fallback: split by sentence markers if no bullets present
        sentences = re.split(r"\.\s+", content)
        return [s.strip() for s in sentences if len(s.strip()) > 20]

    def _contains_title_hint(self, text: str) -> bool:
        lower = text.lower()
        return any(keyword in lower for keyword in TITLE_HINTS)

    def _extract_date_range(self, text: str) -> Optional[str]:
        match = DATE_RANGE_PATTERN.search(text)
        return match.group(0).strip() if match else None

    def _parse_duration(self, duration_string: str) -> Tuple[Optional[date], Optional[date], Optional[str]]:
        if not duration_string:
            return None, None, None

        match = DATE_RANGE_PATTERN.search(duration_string)
        if not match:
            return None, None, duration_string

        start_raw = match.group("start")
        end_raw = match.group("end")
        start_date = self._parse_date_token(start_raw, is_end=False)
        end_date = self._parse_date_token(end_raw, is_end=True)

        return start_date, end_date, duration_string

    def _parse_date_token(self, token: str, is_end: bool = False) -> Optional[date]:
        if not token:
            return None

        token = token.strip()
        lower = token.lower()
        if lower in {"present", "current", "now"}:
            return date.today()

        quarter_match = re.match(r"Q([1-4])\s*(\d{4})", token, re.IGNORECASE)
        if quarter_match:
            quarter = int(quarter_match.group(1))
            year = int(quarter_match.group(2))
            month = quarter * 3 if is_end else ((quarter - 1) * 3) + 1
            return date(year, month, 1)

        month_year_match = re.match(
            r"(?P<month>[A-Za-z]+)\s+(?P<year>\d{4})",
            token,
            re.IGNORECASE,
        )
        if month_year_match:
            month_name = month_year_match.group("month").lower()
            year = int(month_year_match.group("year"))
            month = MONTH_MAP.get(month_name[:3].lower(), 1)
            return date(year, month, 1)

        year_match = re.match(r"^(\d{4})$", token)
        if year_match:
            year = int(year_match.group(1))
            month = 12 if is_end else 1
            return date(year, month, 1)

        return None

    def _remove_date_text(self, text: str, date_text: str) -> str:
        if not date_text:
            return text
        return re.sub(re.escape(date_text), "", text, flags=re.IGNORECASE).strip(" ,|-–—")

    def _calculate_months(self, start_date: date, end_date: date) -> int:
        if not start_date or not end_date:
            return 0

        start_months = start_date.year * 12 + start_date.month
        end_months = end_date.year * 12 + end_date.month
        return max(0, end_months - start_months + 1)

    def _merge_duplicate_entries(self, items: List[Dict]) -> List[Dict]:
        merged = []
        seen = set()
        for item in items:
            canonical = (item.get("company"), item.get("designation"), item.get("start_date"), item.get("end_date"))
            if canonical in seen:
                continue
            seen.add(canonical)
            merged.append(item)
        return merged

    def _summarize_experience(self, items: List[Dict]) -> Dict:
        normalized = [item for item in items if item.get("start_date") and item.get("end_date")]
        sorted_items = sorted(normalized, key=lambda item: item["start_date"])

        merged_ranges = []
        for item in sorted_items:
            start = date.fromisoformat(item["start_date"])
            end = date.fromisoformat(item["end_date"])
            merged_ranges = self._add_range(merged_ranges, start, end)

        total_months = sum(self._calculate_months(start, end) for start, end in merged_ranges)
        gaps = self._detect_gaps(sorted_items)
        overlaps = self._detect_overlaps(sorted_items)

        return {
            "total_experience_months": total_months,
            "total_experience_years": total_months / 12.0,
            "total_roles": len(items),
            "roles_with_dates": len(normalized),
            "merged_ranges": [
                {"start_date": r[0].isoformat(), "end_date": r[1].isoformat()} for r in merged_ranges
            ],
            "gaps": gaps,
            "overlaps": overlaps,
        }

    def _add_range(self, ranges: List[Tuple[date, date]], start: date, end: date) -> List[Tuple[date, date]]:
        if not ranges:
            return [(start, end)]

        merged = []
        inserted = False
        for current_start, current_end in ranges:
            if end < current_start:
                if not inserted:
                    merged.append((start, end))
                    inserted = True
                merged.append((current_start, current_end))
            elif start > current_end:
                merged.append((current_start, current_end))
            else:
                start = min(start, current_start)
                end = max(end, current_end)
        if not inserted:
            merged.append((start, end))
        return merged

    def _detect_gaps(self, items: List[Dict]) -> List[Dict]:
        gaps = []
        previous_end = None
        for item in items:
            start = date.fromisoformat(item["start_date"])
            end = date.fromisoformat(item["end_date"])
            if previous_end and start > previous_end:
                gap_months = self._calculate_months(previous_end, start) - 1
                if gap_months >= self.gap_months_threshold:
                    gaps.append({
                        "gap_start": previous_end.isoformat(),
                        "gap_end": start.isoformat(),
                        "gap_months": gap_months,
                        "between": {
                            "previous_role": items[items.index(item) - 1].get("designation"),
                            "next_role": item.get("designation"),
                        },
                    })
            if not previous_end or end > previous_end:
                previous_end = end
        return gaps

    def _detect_overlaps(self, items: List[Dict]) -> List[Dict]:
        overlaps = []
        for index, item in enumerate(items[:-1]):
            current_start = date.fromisoformat(item["start_date"])
            current_end = date.fromisoformat(item["end_date"])
            next_item = items[index + 1]
            next_start = date.fromisoformat(next_item["start_date"])
            next_end = date.fromisoformat(next_item["end_date"])
            if next_start <= current_end:
                overlap_end = min(current_end, next_end)
                overlap_months = self._calculate_months(next_start, overlap_end)
                if overlap_months > 0:
                    overlaps.append({
                        "role_a": item.get("designation"),
                        "role_b": next_item.get("designation"),
                        "overlap_months": overlap_months,
                        "overlap_period": {
                            "start": next_start.isoformat(),
                            "end": overlap_end.isoformat(),
                        },
                    })
        return overlaps


class RoleSimilarity:
    """Role-to-role similarity utilities."""

    @staticmethod
    def similarity(text_a: Optional[str], text_b: Optional[str]) -> float:
        if not text_a or not text_b:
            return 0.0

        normalized_a = re.sub(r"[^a-z0-9]+", " ", text_a.lower()).strip()
        normalized_b = re.sub(r"[^a-z0-9]+", " ", text_b.lower()).strip()

        if not normalized_a or not normalized_b:
            return 0.0

        return SequenceMatcher(None, normalized_a, normalized_b).ratio()

    @classmethod
    def compare_roles(cls, role_a: Dict, role_b: Dict) -> float:
        title_score = cls.similarity(role_a.get("designation"), role_b.get("designation"))
        company_score = cls.similarity(role_a.get("company"), role_b.get("company"))
        responsibilities_a = " ".join(role_a.get("responsibilities", []))
        responsibilities_b = " ".join(role_b.get("responsibilities", []))
        responsibility_score = cls.similarity(responsibilities_a, responsibilities_b)

        return round((title_score * 0.6) + (responsibility_score * 0.3) + (company_score * 0.1), 3)