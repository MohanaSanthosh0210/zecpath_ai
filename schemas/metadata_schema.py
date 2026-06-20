from dataclasses import dataclass, asdict


@dataclass
class TranscriptMetadata:

    transcript_id: str

    candidate_id: str

    job_id: str

    question_id: str

    timestamp: str

    confidence_level: float

    language: str

    source: str

    processing_version: str

    def to_dict(self):
        return asdict(self)