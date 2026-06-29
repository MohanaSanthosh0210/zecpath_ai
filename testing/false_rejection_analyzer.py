import os
import json


class FalseRejectionAnalyzer:

    INPUT_FILE = (
        "data/comparison/human_vs_ai.json"
    )

    OUTPUT_FILE = (
        "data/optimization/false_rejection_report.json"
    )

    def analyze(self):

        with open(
            self.INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            comparison = json.load(file)

        ai = comparison["ai_decision"].lower()

        human = comparison["human_decision"].lower()

        false_rejection = (

            ai == "review"

            and

            human == "pass"

        )

        false_acceptance = (

            ai == "pass"

            and

            human == "review"

        )

        report = {

            "candidate_id":
                comparison["candidate_id"],

            "false_rejection":
                false_rejection,

            "false_acceptance":
                false_acceptance,

            "recommendation":

                "Reduce screening threshold"

                if false_rejection

                else

                "Current threshold acceptable"

        }

        os.makedirs(
            "data/optimization",
            exist_ok=True
        )

        with open(
            self.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return report


if __name__ == "__main__":

    analyzer = FalseRejectionAnalyzer()

    report = analyzer.analyze()

    print(
        json.dumps(
            report,
            indent=4
        )
    )