import json
from pathlib import Path


class Authentication:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (

        BASE_DIR /

        "config" /

        "authentication.json"

    )

    @staticmethod
    def load():

        with open(

            Authentication.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def get_configuration():

        return Authentication.load()["authentication"]


if __name__ == "__main__":

    print(

        json.dumps(

            Authentication.get_configuration(),

            indent=4

        )

    )