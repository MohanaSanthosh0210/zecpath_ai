import json
from pathlib import Path

from review.system_walkthrough import (
    SystemWalkthrough
)

from review.improvement_tracker import (
    ImprovementTracker
)

from review.action_plan_generator import (
    ActionPlanGenerator
)


class ReviewEngine:

    OUTPUT_DIR = (
        Path("data") /
        "internal_review"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    @staticmethod
    def run():

        walkthrough = (
            SystemWalkthrough.run()
        )

        improvements = (
            ImprovementTracker.generate()
        )

        action_plan = (
            ActionPlanGenerator.generate()
        )

        report = {

            "review_date": "2026-08-06",

            "modules_reviewed": [

                "Resume Parser",

                "ATS Engine",

                "Screening AI",

                "HR Interview AI",

                "Technical Interview AI",

                "Decision AI"

            ],

            "overall_status":
            walkthrough["overall_status"],

            "issues_found":
            len(
                improvements["improvements"]
            ),

            "critical_issues": 0,

            "major_issues": 2,

            "minor_issues": 3

        }

        with open(

            ReviewEngine.OUTPUT_DIR /
            "internal_review_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(
            "Internal review completed successfully."
        )


if __name__ == "__main__":

    ReviewEngine.run()