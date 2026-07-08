import json
import os

from aptitude_evaluation.aptitude_engine import (
    AptitudeEngine
)
from aptitude_evaluation.logical_reasoning_scorer import (
    LogicalReasoningScorer
)
from aptitude_evaluation.problem_solving_analyzer import (
    ProblemSolvingAnalyzer
)
from aptitude_evaluation.scenario_evaluator import (
    ScenarioEvaluator
)


def test_reasoning_model_detects_structured_reasoning():

    answer = (
        "I would first review the issue, explain my reasoning, "
        "and propose a practical solution."
    )

    result = LogicalReasoningScorer.calculate(
        answer,
        ["understand", "reasoning", "solution"]
    )

    assert result["logical_reasoning_score"] >= 60


def test_problem_solving_analysis_detects_clear_process():

    answer = (
        "I would review the problem, test a fix, and confirm the outcome."
    )

    result = ProblemSolvingAnalyzer.analyze(answer)

    assert result["problem_solving_score"] >= 50


def test_scenario_evaluation_detects_contextual_response():

    answer = (
        "I would assess the impact, explain my plan, and communicate with the team."
    )

    result = ScenarioEvaluator.evaluate(
        answer,
        ["impact", "communicate", "plan"]
    )

    assert result["scenario_score"] >= 60


def test_process_supports_hr_question_answer_bundle(tmp_path, monkeypatch):

    answer_dir = tmp_path / "data" / "understood_answers"

    answer_dir.mkdir(parents=True, exist_ok=True)

    answer_data = {
        "candidate_id": "C001",
        "interview_answers": [
            {
                "question_text": "Tell me about a time you solved a problem.",
                "answer_text": "I would analyze the issue, explain the reasoning, and propose a practical solution."
            }
        ]
    }

    bundle_path = answer_dir / "hr_bundle.json"

    with open(bundle_path, "w", encoding="utf-8") as file:
        json.dump(answer_data, file)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(AptitudeEngine, "ANSWER_DIR", str(answer_dir))
    monkeypatch.setattr(AptitudeEngine, "ANSWER_FILE", str(answer_dir / "fallback.json"))
    monkeypatch.setattr(AptitudeEngine, "OUTPUT_FOLDER", str(tmp_path / "data" / "aptitude"))
    monkeypatch.setattr(AptitudeEngine, "OUTPUT_FILE", str(tmp_path / "data" / "aptitude" / "aptitude_report.json"))

    engine = AptitudeEngine()
    report = engine.process()

    assert "analyze" in report["candidate_answer"].lower()
    assert report["candidate_id"] == "C001"


def test_process_uses_latest_understood_answer(tmp_path, monkeypatch):

    answer_dir = tmp_path / "data" / "understood_answers"

    answer_dir.mkdir(parents=True, exist_ok=True)

    old_answer = {
        "structured_answer": {
            "text": "I would review the issue briefly."
        }
    }

    new_answer = {
        "structured_answer": {
            "text": "I would analyze the issue, explain the reasoning, and propose a practical solution."
        }
    }

    old_path = answer_dir / "old_answer.json"
    new_path = answer_dir / "new_answer.json"

    with open(old_path, "w", encoding="utf-8") as file:
        json.dump(old_answer, file)

    with open(new_path, "w", encoding="utf-8") as file:
        json.dump(new_answer, file)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(AptitudeEngine, "ANSWER_DIR", str(answer_dir))
    monkeypatch.setattr(AptitudeEngine, "ANSWER_FILE", str(answer_dir / "fallback.json"))
    monkeypatch.setattr(AptitudeEngine, "OUTPUT_FOLDER", str(tmp_path / "data" / "aptitude"))
    monkeypatch.setattr(AptitudeEngine, "OUTPUT_FILE", str(tmp_path / "data" / "aptitude" / "aptitude_report.json"))

    engine = AptitudeEngine()
    report = engine.process()

    assert report["answer_source"]["source_file"].endswith("new_answer.json")
    assert "analyze" in report["candidate_answer"].lower()


def test_aptitude():

    engine = AptitudeEngine()

    report = engine.process()

    assert isinstance(report, dict)

    assert "aptitude_score" in report

    assert (

        0 <=

        report["aptitude_score"]

        <= 100

    )

    print(

        "\nAptitude Engine Test Passed.\n"

    )

    print(

        report

    )


if __name__ == "__main__":

    test_aptitude()