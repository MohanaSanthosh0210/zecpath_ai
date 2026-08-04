import json
from pathlib import Path

from future_ai.feature_catalog import FeatureCatalog


class InnovationProposal:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "roadmap"
    )

    @staticmethod
    def generate():

        InnovationProposal.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        features = (
            FeatureCatalog.get_all_features()
        )

        proposal = {

            "title":
                "Future AI Innovation Proposal",

            "objective":
                "Enhance the Zecpath AI platform with advanced intelligent capabilities.",

            "proposed_features":
                features,

            "expected_benefits": [

                "Improved hiring accuracy",

                "Better recruiter experience",

                "Personalized candidate guidance",

                "Enterprise-ready AI platform"

            ]

        }

        filepath = (
            InnovationProposal.OUTPUT_DIR /
            "innovation_report.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                proposal,
                file,
                indent=4,
                ensure_ascii=False
            )

        return proposal


if __name__ == "__main__":

    print(
        json.dumps(
            InnovationProposal.generate(),
            indent=4
        )
    )