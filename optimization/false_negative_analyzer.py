import json
from pathlib import Path


class FalseNegativeAnalyzer:

    @staticmethod
    def analyze(candidate):

        issues = []

        if candidate.get("decision") != "Rejected":
            return issues

        if (

            candidate.get("technical_score", 0) >= 80

            and

            candidate.get("hr_score", 0) >= 80

        ):

            issues.append(

                "Possible false rejection."

            )

        if (

            candidate.get("overall_score", 0) >= 85

        ):

            issues.append(

                "High overall score but rejected."

            )

        return issues

    @staticmethod
    def save_report(results, output_dir):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = output_dir / "false_negative_report.json"

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

        "candidate_id": "C201",

        "decision": "Rejected",

        "technical_score": 91,

        "hr_score": 86,

        "overall_score": 88

    }

    print(

        FalseNegativeAnalyzer.analyze(sample)

    )