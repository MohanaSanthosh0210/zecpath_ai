import json
from pathlib import Path


class IntentRefinement:

    @staticmethod
    def validate(intent_data):

        confidence = intent_data.get(

            "intent_confidence",

            0

        )

        detected_intent = intent_data.get(

            "intent",

            "unknown"

        )

        if confidence < 0.60:

            return {

                "intent": detected_intent,

                "status": "needs_review",

                "confidence": confidence,

                "reason":

                    "Intent confidence below threshold."

            }

        return {

            "intent": detected_intent,

            "status": "accepted",

            "confidence": confidence

        }

    @staticmethod
    def save_report(result, output_dir):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = output_dir / "intent_refinement_report.json"

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

        "intent": "answer",

        "intent_confidence": 0.54

    }

    print(

        IntentRefinement.validate(sample)

    )