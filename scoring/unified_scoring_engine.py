from __future__ import annotations

from typing import Any, Dict

from schemas.scoring_weights import ROLE_WEIGHTS


class UnifiedScoringEngine:
    """Combine ATS, screening, and HR interview signals into one hiring score."""

    DEFAULT_WEIGHTS = {
        "ats": 0.40,
        "screening": 0.30,
        "hr_interview": 0.30,
    }

    def __init__(self, weights: Dict[str, float] | None = None):
        self.weights = dict(self.DEFAULT_WEIGHTS)
        if weights:
            self.weights.update(weights)

    @staticmethod
    def _normalize_score(value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _coerce_role(role: Any) -> str:
        return str(role or "").strip().lower()

    def get_role_weights(self, role: Any) -> Dict[str, float]:
        role_name = self._coerce_role(role)
        role_weights = ROLE_WEIGHTS.get(role_name)
        if not role_weights:
            return self.DEFAULT_WEIGHTS

        return {
            "ats": float(role_weights.get("skills", 0.35) + role_weights.get("experience", 0.30)),
            "screening": 0.30,
            "hr_interview": 0.30,
        }

    def calculate(self, *, role: Any, ats_score: Any, screening_score: Any, hr_score: Any, candidate_id: Any = None, job_id: Any = None) -> Dict[str, Any]:
        ats = self._normalize_score(ats_score)
        screening = self._normalize_score(screening_score)
        hr = self._normalize_score(hr_score)

        role_weights = self.get_role_weights(role)
        normalized_weights = {
            "ats": role_weights["ats"],
            "screening": role_weights["screening"],
            "hr_interview": role_weights["hr_interview"],
        }

        weighted_score = (
            ats * normalized_weights["ats"]
            + screening * normalized_weights["screening"]
            + hr * normalized_weights["hr_interview"]
        )

        hiring_fit = round(max(0.0, min(100.0, weighted_score)), 2)

        if hiring_fit >= 85:
            status = "Strong Fit"
        elif hiring_fit >= 70:
            status = "Good Fit"
        elif hiring_fit >= 55:
            status = "Needs Review"
        else:
            status = "Not Fit"

        return {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "role": self._coerce_role(role),
            "round_scores": {
                "ats": round(ats, 2),
                "screening": round(screening, 2),
                "hr_interview": round(hr, 2),
            },
            "weights": normalized_weights,
            "unified_score": round(weighted_score, 2),
            "hiring_fit_percentage": hiring_fit,
            "status": status,
        }


def calculate_unified_score(*, role: Any, ats_score: Any, screening_score: Any, hr_score: Any, candidate_id: Any = None, job_id: Any = None) -> Dict[str, Any]:
    return UnifiedScoringEngine().calculate(
        role=role,
        ats_score=ats_score,
        screening_score=screening_score,
        hr_score=hr_score,
        candidate_id=candidate_id,
        job_id=job_id,
    )
