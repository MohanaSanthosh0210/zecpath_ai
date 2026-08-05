import json
from pathlib import Path


class ScalabilityPlanner:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "scalability.json"
    )

    @staticmethod
    def load():

        with open(
            ScalabilityPlanner.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def get_strategy():

        config = ScalabilityPlanner.load()

        return {

            "architecture": "Microservices",

            "horizontal_scaling":
                config["horizontal_scaling"],

            "load_balancer":
                config["load_balancer"],

            "auto_scaling":
                config["auto_scaling"],

            "database_replication":
                config["database_replication"],

            "max_instances":
                config["max_instances"]

        }


if __name__ == "__main__":

    print(

        json.dumps(

            ScalabilityPlanner.get_strategy(),

            indent=4

        )

    )