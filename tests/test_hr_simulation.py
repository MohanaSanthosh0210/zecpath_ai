from hr_testing.hr_testing_runner import run_day40_hr_simulation


def test_day40_hr_simulation_outputs():
    result = run_day40_hr_simulation()

    assert "simulation_results_path" in result
    assert "accuracy_report_path" in result
    assert "recommendations_path" in result
