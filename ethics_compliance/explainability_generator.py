"""
Day 43 – Ethics & Compliance Review

Explainability Generator

Generates recruiter-friendly explanations for AI decisions.
"""

import json
from pathlib import Path


class ExplainabilityGenerator:

    def __init__(self):

        self.output_dir = Path("data/ethics")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = (
            self.output_dir /
            "explainability_notes.json"
        )

    # ---------------------------------------------------------

    def generate(
        self,
        communication=None,
        confidence=None,
        hr_score=None,
        aptitude=None,
        unified_score=None
    ):

        notes = []

        # ---------------- Communication ----------------

        if communication is not None:

            if communication >= 85:
                notes.append(
                    "Candidate demonstrated excellent communication."
                )

            elif communication >= 70:
                notes.append(
                    "Candidate communication was satisfactory."
                )

            else:
                notes.append(
                    "Communication requires improvement."
                )

        # ---------------- Confidence ----------------

        if confidence is not None:

            if confidence >= 85:
                notes.append(
                    "Candidate appeared confident throughout the interview."
                )

            elif confidence >= 70:
                notes.append(
                    "Candidate showed moderate confidence."
                )

            else:
                notes.append(
                    "Candidate showed hesitation during responses."
                )

        # ---------------- HR ----------------

        if hr_score is not None:

            if hr_score >= 85:
                notes.append(
                    "HR interview responses were consistent and relevant."
                )

            elif hr_score >= 70:
                notes.append(
                    "HR responses were generally acceptable."
                )

            else:
                notes.append(
                    "HR interview performance needs improvement."
                )

        # ---------------- Aptitude ----------------

        if aptitude is not None:

            if aptitude >= 85:
                notes.append(
                    "Strong logical reasoning and problem-solving ability."
                )

            elif aptitude >= 70:
                notes.append(
                    "Reasoning ability is satisfactory."
                )

            else:
                notes.append(
                    "Logical reasoning could be improved."
                )

        # ---------------- Unified ----------------

        if unified_score is not None:

            if unified_score >= 85:
                recommendation = "Strong Hire"

            elif unified_score >= 70:
                recommendation = "Hire"

            elif unified_score >= 60:
                recommendation = "Review"

            else:
                recommendation = "Reject"

        else:

            recommendation = "Not Available"

        report = {

            "explainability_notes": notes,

            "recommendation": recommendation

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


# ---------------------------------------------------------

if __name__ == "__main__":

    generator = ExplainabilityGenerator()

    result = generator.generate(

        communication=92,

        confidence=88,

        hr_score=91,

        aptitude=86,

        unified_score=89

    )

    print(json.dumps(result, indent=4))