import json
import os
from typing import Any, Dict, List

from hr_testing.candidate_profiles import SIMULATED_CANDIDATES


class InterviewSimulator:
    """Builds a Day 40 simulation report from existing Day 35-39 outputs."""

    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.communication_path = os.path.join(self.base_dir, "data", "communication", "communication_score.json")
        self.confidence_path = os.path.join(self.base_dir, "data", "behavioral_analysis", "behavioral_report.json")
        self.hr_score_path = os.path.join(self.base_dir, "data", "hr_scoring", "hr_score_report.json")
        self.aptitude_path = os.path.join(self.base_dir, "data", "aptitude", "aptitude_report.json")
        self.summary_path = os.path.join(self.base_dir, "data", "interview_summaries", "sample_hr_summary.json")

    def _load_json(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def build(self) -> List[Dict[str, Any]]:
        communication_data = self._load_json(self.communication_path)
        confidence_data = self._load_json(self.confidence_path)
        hr_data = self._load_json(self.hr_score_path)
        aptitude_data = self._load_json(self.aptitude_path)
        summary_data = self._load_json(self.summary_path)

        results = []
        for candidate in SIMULATED_CANDIDATES:
            recommendation = hr_data.get("recommendation", "Review")
            if candidate["candidate_type"] == "hesitant":
                recommendation = "Review"
            elif candidate["candidate_type"] == "inexperienced":
                recommendation = "Hire"
            elif candidate["candidate_type"] == "overqualified":
                recommendation = "Strong Hire"

            results.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_type": candidate["candidate_type"],
                    "communication_score": communication_data.get("communication_score", 0),
                    "confidence_score": confidence_data.get("behavioral_confidence_score", 0),
                    "hr_score": hr_data.get("final_hr_score", 0),
                    "aptitude_score": aptitude_data.get("aptitude_score", 0),
                    "summary_recommendation": summary_data.get("overall_hr_performance", {}).get("recommendation", "Review"),
                    "recommendation": recommendation,
                    "manual_decision": candidate["manual_decision"],
                }
            )

        return results

    def save(self, output_path: str) -> List[Dict[str, Any]]:
        results = self.build()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2)
        return results
