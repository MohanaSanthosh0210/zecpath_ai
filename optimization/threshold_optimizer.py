import json
from pathlib import Path


class ThresholdOptimizer:

    @staticmethod
    def optimize(stats, config):

        updates = {

            "selection_threshold":
                config["selection_threshold"],

            "review_threshold":
                config["review_threshold"]

        }

        if (

            stats.get("false_positive_rate", 0)

            >

            config["false_positive_limit"]

        ):

            updates["selection_threshold"] += 5

        if (

            stats.get("false_negative_rate", 0)

            >

            config["false_negative_limit"]

        ):

            updates["review_threshold"] -= 5

        return updates

    @staticmethod
    def save(updates, output_dir):

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        filepath = (

            output_dir /

            "threshold_updates.json"

        )

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                updates,

                file,

                indent=4,

                ensure_ascii=False

            )

        return filepath


if __name__ == "__main__":

    config = {

        "selection_threshold": 80,

        "review_threshold": 60,

        "false_positive_limit": 0.10,

        "false_negative_limit": 0.10

    }

    stats = {

        "false_positive_rate": 0.14,

        "false_negative_rate": 0.03

    }

    print(

        ThresholdOptimizer.optimize(

            stats,

            config

        )

    )