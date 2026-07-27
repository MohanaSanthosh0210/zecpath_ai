"""Schema for unified candidate score object."""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class HiringFitStatus(str, Enum):
    """Hiring fit status categories."""
    STRONG_FIT = "Strong Fit"
    GOOD_FIT = "Good Fit"
    REQUIRES_REVIEW = "Requires Review"
    CONDITIONAL_FIT = "Conditional Fit"
    NOT_FIT = "Not Fit"


@dataclass
class RoundScore:
    """Individual round evaluation score."""
    round_name: str
    score: float
    max_score: float = 100.0
    normalized_score: float = field(default=0.0)
    weight: float = field(default=0.0)
    weighted_contribution: float = field(default=0.0)
    components: Dict[str, float] = field(default_factory=dict)
    feedback: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ScoreWeights:
    """Weights used in aggregation."""
    ats: float = 0.0
    screening: float = 0.0
    hr_interview: float = 0.0
    technical_interview: float = 0.0
    machine_test: float = 0.0
    behavioral_intelligence: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return asdict(self)
    
    def validate(self) -> bool:
        """Validate weights sum to ~1.0."""
        total = sum(self.to_dict().values())
        return abs(total - 1.0) < 0.001


@dataclass
class NormalizationDetails:
    """Details about normalization applied."""
    method: str
    scale_min: float = 0.0
    scale_max: float = 100.0
    outliers_detected: bool = False
    outlier_adjustment: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class UnifiedCandidateScore:
    """Unified hiring intelligence score for a candidate."""
    
    # Candidate and job identifiers
    candidate_id: str
    job_id: Optional[str] = None
    role: str = "general"
    
    # All round scores
    round_scores: Dict[str, RoundScore] = field(default_factory=dict)
    
    # Weights used
    weights: ScoreWeights = field(default_factory=ScoreWeights)
    
    # Calculated scores
    unified_score: float = 0.0  # Weighted average
    hiring_fit_percentage: float = 0.0  # Final hiring fit %
    status: HiringFitStatus = HiringFitStatus.NOT_FIT
    
    # Component breakdown
    component_contributions: Dict[str, float] = field(default_factory=dict)
    
    # Normalization details
    normalization_details: NormalizationDetails = field(default_factory=lambda: NormalizationDetails(method="minmax"))
    
    # Transparency information
    calculation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    calculation_notes: List[str] = field(default_factory=list)
    missing_rounds: List[str] = field(default_factory=list)
    
    # Flags and insights
    red_flags: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    
    # Recommendations
    recommendation: Optional[str] = None
    decision: Optional[str] = None
    
    def add_round_score(self, round_score: RoundScore) -> None:
        """Add a round score to the unified score."""
        self.round_scores[round_score.round_name] = round_score
    
    def add_calculation_note(self, note: str) -> None:
        """Add a calculation note for transparency."""
        self.calculation_notes.append(note)
    
    def add_red_flag(self, flag: str) -> None:
        """Add a red flag."""
        self.red_flags.append(flag)
    
    def add_strength(self, strength: str) -> None:
        """Add a strength."""
        self.strengths.append(strength)
    
    def add_concern(self, concern: str) -> None:
        """Add a concern."""
        self.concerns.append(concern)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "role": self.role,
            "round_scores": {k: v.to_dict() for k, v in self.round_scores.items()},
            "weights": self.weights.to_dict(),
            "unified_score": round(self.unified_score, 2),
            "hiring_fit_percentage": round(self.hiring_fit_percentage, 2),
            "status": self.status.value,
            "component_contributions": {k: round(v, 2) for k, v in self.component_contributions.items()},
            "normalization_details": self.normalization_details.to_dict(),
            "calculation_timestamp": self.calculation_timestamp,
            "calculation_notes": self.calculation_notes,
            "missing_rounds": self.missing_rounds,
            "red_flags": self.red_flags,
            "strengths": self.strengths,
            "concerns": self.concerns,
            "recommendation": self.recommendation,
            "decision": self.decision,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UnifiedCandidateScore":
        """Create from dictionary."""
        score = UnifiedCandidateScore(
            candidate_id=data.get("candidate_id", ""),
            job_id=data.get("job_id"),
            role=data.get("role", "general"),
        )
        score.unified_score = data.get("unified_score", 0.0)
        score.hiring_fit_percentage = data.get("hiring_fit_percentage", 0.0)
        score.status = HiringFitStatus(data.get("status", "Not Fit"))
        score.component_contributions = data.get("component_contributions", {})
        score.calculation_notes = data.get("calculation_notes", [])
        score.missing_rounds = data.get("missing_rounds", [])
        score.red_flags = data.get("red_flags", [])
        score.strengths = data.get("strengths", [])
        score.concerns = data.get("concerns", [])
        score.recommendation = data.get("recommendation")
        score.decision = data.get("decision")
        return score
