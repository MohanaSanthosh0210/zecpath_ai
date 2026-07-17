"""
Day 43 – Ethics & Compliance Review

Consent Manager

Responsibilities
----------------
• Verify candidate consent
• Store consent records
• Validate interview eligibility
"""

import json
from pathlib import Path
from datetime import datetime


class ConsentManager:

    def __init__(self):

        self.output_dir = Path("data/ethics")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = self.output_dir / "candidate_consent.json"

    # -------------------------------------------------------

    def record_consent(
        self,
        candidate_id,
        consent_given=True,
        version="1.0"
    ):

        consent = {
            "candidate_id": candidate_id,
            "consent_given": consent_given,
            "timestamp": datetime.now().isoformat(),
            "policy_version": version
        }

        with open(
            self.output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                consent,
                file,
                indent=4
            )

        return consent

    # -------------------------------------------------------

    def load_consent(self):

        if not self.output_file.exists():

            return None

        with open(
            self.output_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # -------------------------------------------------------

    def verify_consent(self):

        consent = self.load_consent()

        if consent is None:

            return {
                "eligible": False,
                "reason": "Consent record not found."
            }

        if not consent.get("consent_given"):

            return {
                "eligible": False,
                "reason": "Candidate did not provide consent."
            }

        return {
            "eligible": True,
            "reason": "Consent verified."
        }


# ------------------------------------------------------------

if __name__ == "__main__":

    manager = ConsentManager()

    manager.record_consent(
        candidate_id="UNKNOWN",
        consent_given=True
    )

    print(manager.verify_consent())