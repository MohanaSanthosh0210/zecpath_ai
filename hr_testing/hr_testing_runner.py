import os
from hr_testing.accuracy_evaluator import AccuracyEvaluator
from hr_testing.inconsistency_detector import InconsistencyDetector
from hr_testing.interview_simulator import InterviewSimulator
from hr_testing.recommendation_engine import RecommendationEngine


def run_day40_hr_simulation():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    simulator = InterviewSimulator()
    simulation_results = simulator.save(
        os.path.join(base_dir, "data", "simulation_results", "interview_test_report.json")
    )

    evaluator = AccuracyEvaluator()
    evaluator.save(
        simulation_results,
        os.path.join(base_dir, "data", "accuracy_reports", "accuracy_report.json"),
    )

    detector = InconsistencyDetector()
    issues = detector.detect(simulation_results)

    engine = RecommendationEngine()
    engine.save(issues, os.path.join(base_dir, "data", "improvement_reports", "recommendations.json"))

    return {
        "simulation_results_path": os.path.join(base_dir, "data", "simulation_results", "interview_test_report.json"),
        "accuracy_report_path": os.path.join(base_dir, "data", "accuracy_reports", "accuracy_report.json"),
        "recommendations_path": os.path.join(base_dir, "data", "improvement_reports", "recommendations.json"),
    }


if __name__ == "__main__":
    print(run_day40_hr_simulation())
