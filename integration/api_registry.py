import json
from pathlib import Path


class APIRegistry:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "api_registry.json"
    )

    @staticmethod
    def load_registry():

        with open(
            APIRegistry.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_all_apis():

        return APIRegistry.load_registry()["apis"]

    @staticmethod
    def get_api(module_name):

        for api in APIRegistry.get_all_apis():

            if api["module"] == module_name:

                return api

        return None


if __name__ == "__main__":

    print(

        json.dumps(

            APIRegistry.get_all_apis(),

            indent=4

        )

    )