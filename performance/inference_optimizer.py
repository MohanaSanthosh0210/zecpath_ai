import json
from pathlib import Path


class InferenceOptimizer:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "performance_targets.json"
    )

    @staticmethod
    def load_targets():

        with open(
            InferenceOptimizer.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_targets():

        return InferenceOptimizer.load_targets()

    @staticmethod
    def recommendations():

        return {

            "lazy_model_loading": True,

            "shared_model_instances": True,

            "warm_start": True,

            "batch_inference": True

        }


if __name__ == "__main__":

    print(

        json.dumps(

            InferenceOptimizer.recommendations(),

            indent=4

        )

    )