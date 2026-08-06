import json
from datetime import datetime
from pathlib import Path


class ErrorTracker:

    BASE_DIR = Path(__file__).resolve().parent

    LOG_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "error_report.json"
    )

    @staticmethod
    def log(

        error_code,

        message,

        severity

    ):

        ErrorTracker.LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        record = {

            "timestamp":
                datetime.now().isoformat(),

            "error_code":
                error_code,

            "message":
                message,

            "severity":
                severity

        }

        logs = []

        if ErrorTracker.LOG_FILE.exists():

            with open(

                ErrorTracker.LOG_FILE,

                "r",

                encoding="utf-8"

            ) as file:

                logs = json.load(file)

        logs.append(record)

        with open(

            ErrorTracker.LOG_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                logs,

                file,

                indent=4

            )


if __name__ == "__main__":

    ErrorTracker.log(

        "ATS001",

        "Job Description Missing",

        "Medium"

    )

    print("Error Logged")