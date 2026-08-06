from observability.metrics_collector import (
    MetricsCollector
)

from observability.alert_manager import (
    AlertManager
)

from observability.dashboard_designer import (
    DashboardDesigner
)

from observability.observability_engine import (
    ObservabilityEngine
)


def test_observability():

    metrics = (

        MetricsCollector.collect()

    )

    alerts = (

        AlertManager.generate_alert_rules()

    )

    dashboard = (

        DashboardDesigner.create_dashboard()

    )

    summary = (

        ObservabilityEngine.generate_reports()

    )

    assert (
        metrics["system_accuracy_percent"] > 0
    )

    assert (
        "high_response_time"
        in alerts
    )

    assert (
        dashboard["title"]
        ==
        "Zecpath AI Monitoring Dashboard"
    )

    assert (
        summary["system_status"]
        ==
        "Healthy"
    )

    print(
        "Observability Test Passed"
    )


if __name__ == "__main__":

    test_observability()