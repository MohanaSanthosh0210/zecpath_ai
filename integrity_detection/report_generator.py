import json
from pathlib import Path

from integrity_detection.risk_engine import (
    RiskEngine
)


class IntegrityReportGenerator:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "integrity_reports"
    )

    @staticmethod
    def generate(event_summary):

        score = event_summary.get(
            "integrity_score",
            0
        )

        report = {

            "candidate_id": event_summary.get(
                "candidate_id",
                "UNKNOWN"
            ),

            "integrity_score": score,

            "risk_level": (
                RiskEngine.determine_level(score)
            ),

            "events": event_summary.get(
                "events",
                []
            ),

            "warnings": event_summary.get(
                "warnings",
                []
            )

        }

        IntegrityReportGenerator.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        filepath = (
            IntegrityReportGenerator.OUTPUT_DIR /
            "integrity_report.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False
            )
        )

        print(
            f"\nReport saved to:\n{filepath}"
        )

        return report


if __name__ == "__main__":

    sample = {

        "candidate_id": "C101",

        "integrity_score": 62,

        "events": [

            "Repeated tab switching",

            "Screen focus lost"

        ],

        "warnings": [

            "Manual review recommended"

        ]

    }

    IntegrityReportGenerator.generate(sample)