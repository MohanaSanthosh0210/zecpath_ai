import json
from pathlib import Path


class RetryPolicy:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "retry_policy.json"

    )

    @staticmethod
    def load():

        with open(

            RetryPolicy.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def get_policy():

        return RetryPolicy.load()


if __name__ == "__main__":

    print(

        json.dumps(

            RetryPolicy.get_policy(),

            indent=4

        )

    )