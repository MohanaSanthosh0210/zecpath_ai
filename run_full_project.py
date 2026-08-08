import os
import sys
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import main as run_main_workflow
from observability.observability_runner import main as run_observability


def open_dashboard() -> None:
    dashboard_path = ROOT_DIR / "observability" / "data" / "observability" / "dashboard.html"
    if dashboard_path.exists():
        webbrowser.open(dashboard_path.as_uri())
        print(f"Opened dashboard: {dashboard_path}")
    else:
        print("Dashboard file not found yet.")


def main() -> None:
    print("\n========== FULL PROJECT RUN ==========")
    print("Running core workflow...")
    run_main_workflow()

    print("\nRunning observability workflow...")
    run_observability()

    print("\nFull project run completed.")
    print("Artifacts written to:")
    print(f"- {ROOT_DIR / 'data' / 'semantic_matches' / 'resume_scores.json'}")
    print(f"- {ROOT_DIR / 'observability' / 'data' / 'observability' / 'observability_summary.json'}")

    open_dashboard()


if __name__ == "__main__":
    main()
