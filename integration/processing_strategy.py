import json
from pathlib import Path


class ProcessingStrategy:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "processing_modes.json"
    )

    @staticmethod
    def load():

        with open(
            ProcessingStrategy.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_processing_mode(module):

        modes = ProcessingStrategy.load()

        if module in modes["async"]:

            return "async"

        if module in modes["sync"]:

            return "sync"

        return "undefined"

    @staticmethod
    def get_all_modes():

        return ProcessingStrategy.load()


if __name__ == "__main__":

    print(

        json.dumps(

            ProcessingStrategy.get_all_modes(),

            indent=4

        )

    )