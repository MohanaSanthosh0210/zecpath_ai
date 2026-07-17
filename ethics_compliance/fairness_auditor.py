"""
Day 43 – Ethics & Compliance Review

Fairness Auditor

Reviews the AI interview pipeline to ensure
no prohibited demographic information is used.
"""

import json
from pathlib import Path


class FairnessAuditor:

    PROHIBITED_FIELDS = [

        "age",

        "gender",

        "religion",

        "race",

        "ethnicity",

        "marital_status",

        "nationality",

        "political_affiliation",

        "disability",

        "caste"
    ]

    SAFE_FIELDS = [

        "skills",

        "experience",

        "projects",

        "communication",

        "confidence",

        "logical_reasoning",

        "problem_solving",

        "screening_score",

        "hr_score",

        "aptitude_score",

        "ats_score"
    ]

    def __init__(self):

        self.output_dir = Path("data/ethics")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.output_file = (
            self.output_dir /
            "fairness_review.json"
        )

    # -------------------------------------------------------

    def audit_dictionary(
        self,
        data
    ):

        findings = []

        prohibited_found = []

        self._scan(
            data,
            prohibited_found
        )

        if prohibited_found:

            findings.append(
                "Prohibited demographic fields detected."
            )

        else:

            findings.append(
                "No prohibited demographic fields detected."
            )

        report = {

            "fairness_status": (
                "PASS"
                if not prohibited_found
                else "FAIL"
            ),

            "prohibited_fields_found":
                prohibited_found,

            "approved_scoring_fields":
                self.SAFE_FIELDS,

            "review_notes":
                findings

        }

        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return report

    # -------------------------------------------------------

    def _scan(
        self,
        obj,
        detected
    ):

        if isinstance(obj, dict):

            for key, value in obj.items():

                if key.lower() in self.PROHIBITED_FIELDS:

                    detected.append(key)

                self._scan(
                    value,
                    detected
                )

        elif isinstance(obj, list):

            for item in obj:

                self._scan(
                    item,
                    detected
                )


# ------------------------------------------------------------

if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "skills": [
            "Python",
            "SQL"
        ],

        "communication": 92,

        "confidence": 88

    }

    auditor = FairnessAuditor()

    report = auditor.audit_dictionary(sample)

    print(json.dumps(report, indent=4))