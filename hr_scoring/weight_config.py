import json
import os


class WeightConfig:

    CONFIG_PATH = (
        "hr_scoring/config/scoring_weights.json"
    )

    @staticmethod
    def load_weights():

        if not os.path.exists(

            WeightConfig.CONFIG_PATH

        ):

            raise FileNotFoundError(

                "Weight configuration file not found."

            )

        with open(

            WeightConfig.CONFIG_PATH,

            "r",

            encoding="utf-8"

        ) as file:

            weights = json.load(file)

        WeightConfig.validate(weights)

        return weights

    @staticmethod
    def validate(weights):

        total = round(

            sum(weights.values()),

            2

        )

        if total != 1.00:

            raise ValueError(

                f"Invalid weights. Current total = {total}"

            )


if __name__ == "__main__":

    print(

        WeightConfig.load_weights()

    )