"""
Day 43 – Ethics & Compliance Review

Ethics Review Runner

Runs the complete ethics and compliance audit.

Outputs

data/ethics/

    candidate_consent.json
    fairness_review.json
    explainability_notes.json
    compliance_readiness.json
    ethics_review_summary.json
"""

import json

from pathlib import Path

from ethics_compliance.consent_manager import ConsentManager
from ethics_compliance.fairness_auditor import FairnessAuditor
from ethics_compliance.explainability_generator import (
    ExplainabilityGenerator
)
from ethics_compliance.compliance_checker import (
    ComplianceChecker
)


class EthicsReviewRunner:

    def __init__(self):

        self.output_dir = Path("data/ethics")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.summary_file = (
            self.output_dir /
            "ethics_review_summary.json"
        )

    # ---------------------------------------------------------

    def run(self):

        print("\n========== ETHICS REVIEW ==========\n")

        # ------------------------------------------
        # Consent
        # ------------------------------------------

        consent_manager = ConsentManager()

        consent = consent_manager.record_consent(
            candidate_id="UNKNOWN",
            consent_given=True
        )

        consent_status = consent_manager.verify_consent()

        # ------------------------------------------
        # Fairness
        # ------------------------------------------

        fairness = FairnessAuditor()

        pipeline_sample = {

            "skills": [
                "Python",
                "Machine Learning"
            ],

            "communication": 92,

            "confidence": 88,

            "hr_score": 90,

            "aptitude_score": 86
        }

        fairness_report = fairness.audit_dictionary(
            pipeline_sample
        )

        # ------------------------------------------
        # Explainability
        # ------------------------------------------

        explainability = ExplainabilityGenerator()

        explainability_report = explainability.generate(

            communication=92,

            confidence=88,

            hr_score=90,

            aptitude=86,

            unified_score=89

        )

        # ------------------------------------------
        # Compliance
        # ------------------------------------------

        checker = ComplianceChecker()

        compliance_report = checker.evaluate(

            consent_verified=consent_status[
                "eligible"
            ],

            fairness_verified=(
                fairness_report[
                    "fairness_status"
                ]
                == "PASS"
            ),

            explainability_available=True,

            demographic_bias_removed=True,

            transcript_retention_defined=True,

            candidate_deletion_supported=True

        )

        # ------------------------------------------
        # Final Summary
        # ------------------------------------------

        summary = {

            "consent":

                consent_status,

            "fairness":

                fairness_report,

            "explainability":

                explainability_report,

            "compliance":

                compliance_report

        }

        with open(

            self.summary_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4

            )

        print(

            json.dumps(

                summary,

                indent=4

            )

        )

        print("\nSummary saved to:")

        print(self.summary_file)

        return summary


# ------------------------------------------------------------

if __name__ == "__main__":

    EthicsReviewRunner().run()