import json
from pathlib import Path

from observability.metrics_collector import (
    MetricsCollector
)

from observability.alert_manager import (
    AlertManager
)

from observability.dashboard_designer import (
    DashboardDesigner
)


class ObservabilityEngine:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "observability"
    )

    @staticmethod
    def generate_reports():

        ObservabilityEngine.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        metrics = (
            MetricsCollector.collect()
        )

        alerts = (
            AlertManager.generate_alert_rules()
        )

        dashboard = (
            DashboardDesigner.create_dashboard()
        )

        summary = {

            "system_status":
                "Healthy",

            "observability_enabled":
                True,

            "logging":
                True,

            "monitoring":
                True,

            "alerting":
                True,

            "audit_logging":
                True,

            "metrics":

                metrics,

            "dashboard":

                dashboard["title"]

        }

        with open(

            ObservabilityEngine.OUTPUT_DIR /
            "observability_summary.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4,

                ensure_ascii=False

            )

        return summary


if __name__ == "__main__":

    print(

        json.dumps(

            ObservabilityEngine.generate_reports(),

            indent=4

        )

    )