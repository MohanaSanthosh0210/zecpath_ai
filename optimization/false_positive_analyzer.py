import json
from pathlib import Path


class FalsePositiveAnalyzer:

    @staticmethod
    def analyze(candidate):

        issues = []

        if candidate.get("decision") != "Selected":
            return issues

        if candidate.get("integrity_score", 100) < 50:

            issues.append(
                "Low integrity score despite selection."
            )

        if candidate.get("technical_score", 100) < 60:

            issues.append(
                "Weak technical performance."
            )

        if candidate.get("behavior_score", 100) < 50:

            issues.append(
                "Poor behavioral assessment."
            )

        return issues

    @staticmethod
    def save_report(results, output_dir):

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        filepath = output_dir / "false_positive_report.json"

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                indent=4,
                ensure_ascii=False
            )

        return filepath


if __name__ == "__main__":

    sample = {

        "candidate_id": "C101",

        "decision": "Selected",

        "technical_score": 55,

        "integrity_score": 42,

        "behavior_score": 48

    }

    print(

        FalsePositiveAnalyzer.analyze(sample)

    )