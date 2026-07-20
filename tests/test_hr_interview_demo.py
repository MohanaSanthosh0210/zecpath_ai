import json
import os

from hr_interview.demo_runner import HRInterviewDemoRunner


def test_hr_interview_demo_runner_creates_outputs(tmp_path):
    output_dir = tmp_path / "hr_interview"
    output_dir.mkdir(parents=True, exist_ok=True)

    runner = HRInterviewDemoRunner(output_dir=str(output_dir))
    report = runner.run()

    assert isinstance(report, dict)
    assert report["status"] == "ready_for_demo"
    assert report["final_recommendation"] in {"Strong Hire", "Hire", "Review", "Reject"}

    demo_dataset_path = output_dir / "demo_dataset.json"
    feedback_path = output_dir / "manager_evaluation_feedback.json"
    report_path = output_dir / "final_demo_report.json"

    assert demo_dataset_path.exists()
    assert feedback_path.exists()
    assert report_path.exists()

    demo_payload = json.loads(demo_dataset_path.read_text(encoding="utf-8"))
    assert "candidate_profile" in demo_payload
    assert "interview_flow" in demo_payload
    assert "simulated_answers" in demo_payload
