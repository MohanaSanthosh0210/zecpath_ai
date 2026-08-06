import json
from datetime import datetime
from pathlib import Path


class ModelLogger:

    BASE_DIR = Path(__file__).resolve().parent

    LOG_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "model_logs.json"
    )

    @staticmethod
    def log(

        model,

        prediction,

        confidence,

        inference_time_ms

    ):

        ModelLogger.LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        record = {

            "timestamp":
                datetime.now().isoformat(),

            "model":
                model,

            "prediction":
                prediction,

            "confidence":
                confidence,

            "inference_time_ms":
                inference_time_ms

        }

        logs = []

        if ModelLogger.LOG_FILE.exists():

            with open(

                ModelLogger.LOG_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                logs = json.load(file)

        logs.append(record)

        with open(

            ModelLogger.LOG_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                logs,

                file,

                indent=4

            )


if __name__ == "__main__":

    ModelLogger.log(

        "ATS Engine",

        "Eligible",

        0.94,

        130

    )

    print("Model Log Created")