import json
from pathlib import Path


class ScalabilityPlanner:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "scalability_plan.json"
    )

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "roadmap"
    )

    @staticmethod
    def load_plan():

        with open(
            ScalabilityPlanner.CONFIG,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def generate():

        ScalabilityPlanner.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        plan = (
            ScalabilityPlanner.load_plan()
        )

        report = {

            "deployment":

                plan["deployment_model"],

            "architecture":

                plan["architecture"],

            "database":

                plan["database"],

            "cloud_features": {

                "multi_tenant":

                    plan["multi_tenant"],

                "api_gateway":

                    plan["api_gateway"],

                "load_balancing":

                    plan["load_balancing"],

                "global_scaling":

                    plan["global_scaling"]

            }

        }

        filepath = (
            ScalabilityPlanner.OUTPUT_DIR /
            "scalability_plan.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        return report


if __name__ == "__main__":

    print(
        json.dumps(
            ScalabilityPlanner.generate(),
            indent=4
        )
    )