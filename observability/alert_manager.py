import json
from pathlib import Path


class AlertManager:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "alerts.json"
    )

    OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "alert_rules.json"
    )

    @staticmethod
    def load_thresholds():

        with open(
            AlertManager.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def generate_alert_rules():

        thresholds = (
            AlertManager.load_thresholds()
        )

        rules = {

            "high_response_time": {

                "threshold_ms":
                    thresholds[
                        "response_time_threshold_ms"
                    ],

                "action":
                    "Generate Warning"

            },

            "high_failure_rate": {

                "threshold_percent":
                    thresholds[
                        "failure_rate_threshold_percent"
                    ],

                "action":
                    "Critical Alert"

            },

            "low_accuracy": {

                "threshold_percent":
                    thresholds[
                        "accuracy_threshold_percent"
                    ],

                "action":
                    "Model Review"

            },

            "critical_errors": {

                "threshold":
                    thresholds[
                        "critical_error_threshold"
                    ],

                "action":
                    "Immediate Investigation"

            }

        }

        AlertManager.OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(

            AlertManager.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                rules,

                file,

                indent=4

            )

        return rules


if __name__ == "__main__":

    print(

        json.dumps(

            AlertManager.generate_alert_rules(),

            indent=4

        )

    )