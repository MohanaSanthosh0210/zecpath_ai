from dataclasses import dataclass, field
from typing import List


@dataclass
class InterviewContext:
    """
    Maintains the current interview session state.
    """

    candidate_id: str

    candidate_name: str

    role: str

    experience_years: float

    experience_level: str = ""

    current_stage: str = "INTRODUCTION"

    current_question_index: int = 0

    asked_questions: List[str] = field(default_factory=list)

    scores: dict = field(default_factory=dict)

    interview_completed: bool = False