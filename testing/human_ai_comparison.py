import os
import json


class HumanAIComparison:

    def __init__(self):

        self.screening_path = (
            "data/screening_scores/final_scores/unknown.json"
        )

    def load_ai_result(self):

        with open(
            self.screening_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def compare(
        self,
        human_decision
    ):

        ai_result = self.load_ai_result()

        ai_decision = ai_result.get(
            "status",
            "Review"
        )

        comparison = {

            "candidate_id":
                ai_result.get(
                    "candidate_id",
                    "unknown"
                ),

            "ai_decision":
                ai_decision,

            "human_decision":
                human_decision,

            "match":
                ai_decision.lower()
                ==
                human_decision.lower()

        }

        os.makedirs(
            "data/comparison",
            exist_ok=True
        )

        with open(
            "data/comparison/human_vs_ai.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                comparison,
                file,
                indent=4
            )

        return comparison


if __name__ == "__main__":

    comparator = HumanAIComparison()

    result = comparator.compare(
        human_decision="Pass"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )