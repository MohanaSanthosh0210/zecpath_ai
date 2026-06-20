from dataclasses import dataclass, asdict


@dataclass
class ScreeningInteraction:

    interaction_id: str

    candidate_id: str

    job_id: str

    question_id: str

    question_text: str

    answer_text: str

    answer_type: str

    timestamp: str

    confidence_score: float

    sentiment_score: float

    duration_seconds: float

    language: str

    def to_dict(self):
        return asdict(self)