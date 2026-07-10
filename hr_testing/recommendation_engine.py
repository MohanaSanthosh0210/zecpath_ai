import json
import os
from typing import Any, Dict, List


class RecommendationEngine:
    """Generates tuning suggestions from flagged inconsistencies."""

    def generate(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        recommendations = []
        if any("High confidence" in issue["issue"] for issue in issues):
            recommendations.append("Reduce false rejection threshold")
        if any("High aptitude" in issue["issue"] for issue in issues):
            recommendations.append("Increase weight of aptitude score")
        if any("High confidence" in issue["issue"] for issue in issues):
            recommendations.append("Improve confidence scoring calibration")
        if any("communication" in issue["issue"].lower() for issue in issues):
            recommendations.append("Review communication scoring weights")

        if not recommendations:
            recommendations = [
                "No major inconsistencies detected",
                "Continue monitoring with future interview batches",
            ]

        return {
            "issues_found": len(issues),
            "recommendations": recommendations,
        }

    def save(self, issues: List[Dict[str, Any]], output_path: str) -> Dict[str, Any]:
        report = self.generate(issues)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        return report
