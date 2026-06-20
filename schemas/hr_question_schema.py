from dataclasses import dataclass, asdict


@dataclass
class HRQuestion:
    """
    Standard HR Screening Question Object
    """

    question_id: str

    role: str

    category: str

    question: str

    answer_type: str

    mandatory: bool

    importance: int

    language: str = "en"

    scoring_weight: float = 1.0

    follow_up_allowed: bool = True

    def to_dict(self):
        return asdict(self)