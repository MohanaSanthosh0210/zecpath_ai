import json
import os

from final_system.day56_runner import run_day56_full_system_simulation
from final_system.system_pipeline import AIScreeningPipeline


def test_day56_full_system_simulation_outputs():
    pipeline_result = AIScreeningPipeline().run()
    hr_result = run_day56_full_system_simulation()

    assert pipeline_result is not None
    assert os.path.exists(hr_result["simulation_results_path"])
    assert os.path.exists(hr_result["accuracy_report_path"])
    assert os.path.exists(hr_result["recommendations_path"])

    full_report_path = os.path.join("data", "simulation_results", "day56_full_system_report.json")
    assert os.path.exists(full_report_path)

    with open(full_report_path, "r", encoding="utf-8") as handle:
        report = json.load(handle)

    assert "summary" in report
    assert "performance_analysis" in report
    assert "improvement_recommendations" in report
    assert "comparison_with_human_judgment" in report