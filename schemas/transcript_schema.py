from dataclasses import dataclass, asdict
from typing import List


@dataclass
class TranscriptSegment:
    speaker: str
    question_id: str
    timestamp: str
    text: str
    confidence: float

    def to_dict(self):
        return asdict(self)


@dataclass
class VoiceTranscript:
    transcript_id: str
    candidate_id: str
    job_id: str
    language: str
    interview_date: str
    segments: List[TranscriptSegment]

    def to_dict(self):
        return {
            "transcript_id": self.transcript_id,
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "language": self.language,
            "interview_date": self.interview_date,
            "segments": [
                segment.to_dict()
                for segment in self.segments
            ]
        }