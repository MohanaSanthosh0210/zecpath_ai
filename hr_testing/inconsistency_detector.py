from typing import Any, Dict, List


class InconsistencyDetector:
    """Finds mismatches between confidence, aptitude, and recommendation."""

    def detect(self, simulation_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        issues = []
        for item in simulation_results:
            confidence = item.get("confidence_score", 0)
            aptitude = item.get("aptitude_score", 0)
            recommendation = item.get("recommendation", "Review")

            if confidence >= 90 and recommendation in {"Review", "Reject"}:
                issues.append({
                    "candidate_id": item["candidate_id"],
                    "issue": "High confidence but low recommendation",
                })
            elif aptitude >= 80 and recommendation == "Review":
                issues.append({
                    "candidate_id": item["candidate_id"],
                    "issue": "High aptitude score but only Review recommendation",
                })
            elif item.get("communication_score", 0) >= 85 and item.get("hr_score", 0) < 70:
                issues.append({
                    "candidate_id": item["candidate_id"],
                    "issue": "Excellent communication but low HR score",
                })

        return issues
