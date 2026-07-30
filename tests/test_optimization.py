from optimization.optimization_engine import (
    OptimizationEngine
)


def test_optimization():

    sample = {

        "candidate_id": "TEST001",

        "decision": "Selected",

        "technical_score": 85,

        "integrity_score": 90,

        "behavior_score": 92,

        "ats_score": 84,

        "screening_score": 82,

        "hr_score": 88,

        "intent_confidence": 0.90

    }

    result = OptimizationEngine.optimize(

        sample

    )

    assert (

        result["system_status"]

        ==

        "Optimized"

    )

    print(

        "\nOptimization Test Passed."

    )


if __name__ == "__main__":

    test_optimization()