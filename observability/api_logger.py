import json
from datetime import datetime
from pathlib import Path


class APILogger:

    BASE_DIR = Path(__file__).resolve().parent

    LOG_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "api_logs.json"
    )

    @staticmethod
    def log(
        endpoint,
        method,
        status_code,
        response_time_ms
    ):

        APILogger.LOG_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        log = {

            "timestamp":
                datetime.now().isoformat(),

            "endpoint":
                endpoint,

            "method":
                method,

            "status_code":
                status_code,

            "response_time_ms":
                response_time_ms

        }

        logs = []

        if APILogger.LOG_FILE.exists():

            with open(
                APILogger.LOG_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                logs = json.load(file)

        logs.append(log)

        with open(
            APILogger.LOG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                logs,
                file,
                indent=4
            )


if __name__ == "__main__":

    APILogger.log(

        "/api/ats/score",

        "POST",

        200,

        420

    )

    print("API Log Created")