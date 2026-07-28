import json
import os


class DecisionEngine:

    def __init__(self):

        rules_path = os.path.join(
            os.path.dirname(__file__),
            "config",
            "decision_rules.json"
        )

        with open(
            rules_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.rules = json.load(file)

    def decide(
        self,
        hiring_fit,
        integrity_score,
        behavior_score
    ):

        selected = self.rules["selected"]

        review = self.rules["review"]

        if (

            hiring_fit >= selected["min_hiring_fit"]

            and

            integrity_score >= selected["min_integrity"]

            and

            behavior_score >= selected["min_behavior"]

        ):

            return "Selected"

        if (

            hiring_fit >= review["min_hiring_fit"]

            and

            integrity_score >= review["min_integrity"]

            and

            behavior_score >= review["min_behavior"]

        ):

            return "Hold / Review"

        return "Rejected"