import json
from pathlib import Path


class BatchingManager:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "batching.json"

    )

    @staticmethod
    def load():

        with open(

            BatchingManager.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def get_batch_configuration():

        return BatchingManager.load()


if __name__ == "__main__":

    print(

        json.dumps(

            BatchingManager.get_batch_configuration(),

            indent=4

        )

    )