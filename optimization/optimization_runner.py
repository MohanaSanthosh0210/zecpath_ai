from optimization.optimization_engine import (
    OptimizationEngine
)


def main():

    sample_candidate = {

        "candidate_id": "C001",

        "decision": "Selected",

        "technical_score": 88,

        "integrity_score": 93,

        "behavior_score": 90,

        "ats_score": 86,

        "screening_score": 84,

        "hr_score": 89,

        "intent_confidence": 0.95

    }

    OptimizationEngine.optimize(

        sample_candidate

    )

    print(

        "\nOptimization Completed Successfully."

    )


if __name__ == "__main__":

    main()