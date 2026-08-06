import json
from pathlib import Path


class DashboardDesigner:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG = (
        BASE_DIR /
        "config" /
        "dashboard.json"
    )

    OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "dashboard_design.json"
    )

    @staticmethod
    def create_dashboard():

        with open(

            DashboardDesigner.CONFIG,

            "r",

            encoding="utf-8"

        ) as file:

            config = json.load(file)

        dashboard = {

            "title":

                "Zecpath AI Monitoring Dashboard",

            "sections":

                config["sections"],

            "refresh_interval_seconds":

                30

        }

        DashboardDesigner.OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(

            DashboardDesigner.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                dashboard,

                file,

                indent=4

            )

        return dashboard


if __name__ == "__main__":

    print(

        json.dumps(

            DashboardDesigner.create_dashboard(),

            indent=4

        )

    )