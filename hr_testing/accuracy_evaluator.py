import json
import os
from typing import Any, Dict, List


class AccuracyEvaluator:
    """Compares AI recommendations to manual recruiter decisions."""

    def evaluate(self, simulation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_candidates = len(simulation_results)
        correct_matches = sum(1 for item in simulation_results if item.get("recommendation") == item.get("manual_decision"))
        accuracy = round((correct_matches / total_candidates) * 100, 2) if total_candidates else 0.0

        comparisons = []
        for item in simulation_results:
            comparisons.append(
                {
                    "candidate_id": item["candidate_id"],
                    "ai_decision": item.get("recommendation"),
                    "manual_decision": item.get("manual_decision"),
                    "match": item.get("recommendation") == item.get("manual_decision"),
                }
            )

        return {
            "total_candidates": total_candidates,
            "correct_matches": correct_matches,
            "accuracy": accuracy,
            "comparisons": comparisons,
        }

    def save(self, simulation_results: List[Dict[str, Any]], output_path: str) -> Dict[str, Any]:
        report = self.evaluate(simulation_results)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        return report
