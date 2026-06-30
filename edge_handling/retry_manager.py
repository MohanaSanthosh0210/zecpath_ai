import os
import json


class RetryManager:

    MAX_RETRIES = 2

    OUTPUT_FILE = (
        "data/retries/retry_log.json"
    )

    def __init__(self):

        self.retry_count = 0

        # Create initial retry log
        self.save_log(
            reason=None,
            status="No Retry Required"
        )

    def should_retry(self):

        return self.retry_count < self.MAX_RETRIES

    def save_log(
        self,
        reason,
        status
    ):

        log = {

            "retry_count":
                self.retry_count,

            "reason":
                reason,

            "status":
                status

        }

        os.makedirs(
            "data/retries",
            exist_ok=True
        )

        with open(
            self.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                log,
                file,
                indent=4
            )

        return log

    def retry(
        self,
        reason
    ):

        self.retry_count += 1

        if self.should_retry():

            status = "Retry"

        else:

            status = "Max retries reached"

        return self.save_log(
            reason,
            status
        )