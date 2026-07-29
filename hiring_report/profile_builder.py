import json
from pathlib import Path


class CandidateProfileBuilder:

    BASE_DIR = Path(__file__).resolve().parent

    PROFILE_DIR = (
        BASE_DIR /
        "data" /
        "profiles"
    )

    @staticmethod
    def build(candidate_data):

        profile = {

            "candidate_id":

                candidate_data.get(
                    "candidate_id",
                    "UNKNOWN"
                ),

            "role":

                candidate_data.get(
                    "role",
                    "UNKNOWN"
                ),

            "ats_summary":

                candidate_data.get(
                    "ats_summary",
                    {}
                ),

            "screening_summary":

                candidate_data.get(
                    "screening_summary",
                    {}
                ),

            "hr_summary":

                candidate_data.get(
                    "hr_summary",
                    {}
                ),

            "technical_summary":

                candidate_data.get(
                    "technical_summary",
                    {}
                ),

            "behavior_summary":

                candidate_data.get(
                    "behavior_summary",
                    {}
                ),

            "integrity_summary":

                candidate_data.get(
                    "integrity_summary",
                    {}
                ),

            "overall_score":

                candidate_data.get(
                    "overall_score",
                    {}
                ),

            "final_decision":

                candidate_data.get(
                    "final_decision",
                    {}
                )

        }

        CandidateProfileBuilder.PROFILE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        filepath = (
            CandidateProfileBuilder.PROFILE_DIR /
            "candidate_profile.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False
            )

        return profile


if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "role": "Software Engineer",

        "ats_summary": {
            "score": 88
        },

        "screening_summary": {
            "score": 84
        },

        "hr_summary": {
            "score": 82
        },

        "technical_summary": {
            "score": 90
        },

        "behavior_summary": {
            "score": 85
        },

        "integrity_summary": {
            "score": 92
        },

        "overall_score": {
            "hiring_fit": 88
        },

        "final_decision": {
            "decision": "Selected"
        }

    }

    print(

        json.dumps(

            CandidateProfileBuilder.build(sample),

            indent=4

        )

    )