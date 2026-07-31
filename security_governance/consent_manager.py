import json
from pathlib import Path


class ConsentManager:

    @staticmethod
    def verify(candidate):

        consent = candidate.get(

            "consent",

            False

        )

        return {

            "candidate_id":

                candidate.get(

                    "candidate_id"

                ),

            "consent":

                consent,

            "status":

                "Approved"

                if consent

                else

                "Denied"

        }

    @staticmethod
    def save(result, output_dir):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "consent_report.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                result,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


if __name__ == "__main__":

    sample = {

        "candidate_id": "C001",

        "consent": True

    }

    print(

        ConsentManager.verify(

            sample

        )

    )