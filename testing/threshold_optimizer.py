import os
import json


class ThresholdOptimizer:

    INPUT_FILE = (
        "data/optimization/false_rejection_report.json"
    )

    OUTPUT_FILE = (
        "data/optimized/optimized_thresholds.json"
    )

    def optimize(self):

        with open(
            self.INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)

        screening_threshold = 75
        confidence_threshold = 60

        if report["false_rejection"]:

            screening_threshold -= 5
            confidence_threshold -= 5

        result = {

            "screening_threshold":
                screening_threshold,

            "confidence_threshold":
                confidence_threshold,

            "optimization":
                "Thresholds reduced"

                if report["false_rejection"]

                else

                "No changes required"

        }

        os.makedirs(
            "data/optimized",
            exist_ok=True
        )

        with open(
            self.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4
            )

        return result


if __name__ == "__main__":

    optimizer = ThresholdOptimizer()

    result = optimizer.optimize()

    print(
        json.dumps(
            result,
            indent=4
        )
    )