import os
import json
from typing import Any, Dict, List

from final_system.day56_simulation import Day56FullSystemSimulation
from hr_testing.hr_testing_runner import run_day40_hr_simulation


def run_day56_full_system_simulation() -> Dict[str, Any]:
    hr_result = run_day40_hr_simulation()

    simulation_results_path = hr_result["simulation_results_path"]
    accuracy_report_path = hr_result["accuracy_report_path"]
    recommendations_path = hr_result["recommendations_path"]

    with open(simulation_results_path, "r", encoding="utf-8") as handle:
        simulation_results = json.load(handle)

    with open(accuracy_report_path, "r", encoding="utf-8") as handle:
        accuracy_report = json.load(handle)

    with open(recommendations_path, "r", encoding="utf-8") as handle:
        recommendations_report = json.load(handle)

    issues = []
    for issue in recommendations_report.get("recommendations", []):
        issues.append({"issue": issue})

    simulator = Day56FullSystemSimulation()
    report = simulator.build_report(simulation_results, issues, accuracy_report)
    output_path = simulator.save_report(report)

    return {
        "report_path": output_path,
        "simulation_results_path": simulation_results_path,
        "accuracy_report_path": accuracy_report_path,
        "recommendations_path": recommendations_path,
    }


if __name__ == "__main__":
    print(json.dumps(run_day56_full_system_simulation(), indent=2))