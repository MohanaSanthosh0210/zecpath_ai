import json
from pathlib import Path


class CachingStrategy:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "cache_policy.json"

    )

    @staticmethod
    def load():

        with open(

            CachingStrategy.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def get_policy():

        return CachingStrategy.load()


if __name__ == "__main__":

    print(

        json.dumps(

            CachingStrategy.get_policy(),

            indent=4

        )

    )