from technical_scoring.technical_scoring_engine import (
    TechnicalScoringEngine
)


def run_test():

    sample = {

        "candidate_id": "TEST",

        "question_id": "Q001",

        "difficulty": "medium",

        "accuracy_score": 90,

        "depth_score": 80,

        "reasoning_score": 85,

        "applicability_score": 88

    }

    result = TechnicalScoringEngine.evaluate(sample)

    assert "normalized_score" in result

    assert "skill_breakdown" in result

    print("\nTechnical Scoring Test Passed.\n")

    print(result)


if __name__ == "__main__":

    run_test()