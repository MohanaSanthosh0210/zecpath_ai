import json
from pathlib import Path


class FeatureCatalog:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "future_features.json"
    )

    @staticmethod
    def load_features():

        with open(
            FeatureCatalog.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_all_features():

        return (
            FeatureCatalog.load_features()
            ["future_features"]
        )

    @staticmethod
    def get_by_priority(priority):

        features = (
            FeatureCatalog.get_all_features()
        )

        return [

            feature

            for feature in features

            if feature["priority"].lower()

            ==

            priority.lower()

        ]

    @staticmethod
    def get_by_status(status):

        features = (
            FeatureCatalog.get_all_features()
        )

        return [

            feature

            for feature in features

            if feature["status"].lower()

            ==

            status.lower()

        ]


if __name__ == "__main__":

    print(

        json.dumps(

            FeatureCatalog.get_all_features(),

            indent=4

        )

    )