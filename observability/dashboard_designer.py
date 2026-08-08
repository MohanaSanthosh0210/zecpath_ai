import json
from pathlib import Path
from html import escape


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

    HTML_OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "observability" /
        "dashboard.html"
    )

    @staticmethod
    def _build_html_page(dashboard: dict) -> str:
        sections = dashboard.get("sections", [])
        metrics = dashboard.get("metrics", {})
        alerts = dashboard.get("alerts", {})

        metric_cards = []
        for key, value in metrics.items():
            metric_cards.append(
                f"<div class='card'><h3>{escape(key.replace('_', ' ').title())}</h3><p>{escape(str(value))}</p></div>"
            )

        alert_cards = []
        for key, value in alerts.items():
            alert_cards.append(
                f"<div class='card alert'><h3>{escape(key.replace('_', ' ').title())}</h3><p>{escape(str(value))}</p></div>"
            )

        section_list = "".join(f"<li>{escape(section)}</li>" for section in sections)

        performance_bar = ""
        if metrics:
            accuracy = metrics.get("system_accuracy_percent", 0)
            failure = metrics.get("failure_rate_percent", 0)
            response_time = metrics.get("average_response_time_ms", 0)
            performance_bar = f"""
            <div class='chart-row'>
              <div class='bar-box'><div class='bar-label'>Accuracy</div><div class='bar'><div class='fill good' style='width:{min(100, max(0, accuracy))}%'></div></div><span>{accuracy}%</span></div>
              <div class='bar-box'><div class='bar-label'>Failure Rate</div><div class='bar'><div class='fill warn' style='width:{min(100, max(0, failure * 10))}%'></div></div><span>{failure}%</span></div>
              <div class='bar-box'><div class='bar-label'>Response Time</div><div class='bar'><div class='fill info' style='width:{min(100, max(0, response_time / 10))}%'></div></div><span>{response_time} ms</span></div>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <title>{escape(dashboard['title'])}</title>
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 24px; background: linear-gradient(135deg, #f8fafc, #eef2ff); color: #1f2937; }}
    .page {{ max-width: 1200px; margin: 0 auto; }}
    .hero {{ background: linear-gradient(90deg, #2563eb, #7c3aed); color: white; border-radius: 16px; padding: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    .subtitle {{ opacity: 0.95; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 20px; }}
    .card {{ background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #e5e7eb; }}
    .card h3 {{ margin-top: 0; color: #374151; }}
    .card p {{ font-size: 20px; font-weight: 600; margin: 6px 0 0; color: #111827; }}
    .alert {{ border-left: 6px solid #dc2626; }}
    .chart-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 20px; }}
    .bar-box {{ background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #e5e7eb; }}
    .bar-label {{ font-weight: 600; margin-bottom: 6px; color: #374151; }}
    .bar {{ height: 8px; background: #e5e7eb; border-radius: 999px; overflow: hidden; margin: 8px 0; }}
    .fill {{ height: 100%; border-radius: 999px; }}
    .fill.good {{ background: linear-gradient(90deg, #16a34a, #4ade80); }}
    .fill.warn {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
    .fill.info {{ background: linear-gradient(90deg, #2563eb, #60a5fa); }}
    ul {{ padding-left: 18px; color: #374151; }}
  </style>
</head>
<body>
  <div class='page'>
    <div class='hero'>
      <h1>{escape(dashboard['title'])}</h1>
      <div class='subtitle'>Operational view for candidate processing, interview analytics, and model health.</div>
      <p>Refresh interval: {escape(str(dashboard.get('refresh_interval_seconds', 30)))}s</p>
    </div>

    <h2>Dashboard Sections</h2>
    <ul>{section_list}</ul>

    {performance_bar}

    <h2>Key Metrics</h2>
    <div class='grid'>{''.join(metric_cards)}</div>

    <h2>Active Alerts</h2>
    <div class='grid'>{''.join(alert_cards)}</div>
  </div>
</body>
</html>
"""

    @staticmethod
    def create_dashboard(metrics=None, alerts=None):

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

                30,
            "metrics": metrics or {},
            "alerts": alerts or {}

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

        html_content = DashboardDesigner._build_html_page(dashboard)
        with open(
            DashboardDesigner.HTML_OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(html_content)

        return dashboard


if __name__ == "__main__":

    print(

        json.dumps(

            DashboardDesigner.create_dashboard(),

            indent=4

        )

    )