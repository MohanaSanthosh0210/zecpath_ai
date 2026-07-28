import json
import os

from decision_ai.decision_engine import (
    DecisionEngine
)

from decision_ai.risk_analyzer import (
    RiskAnalyzer
)

from decision_ai.confidence_calculator import (
    ConfidenceCalculator
)

from decision_ai.recommendation_engine import (
    RecommendationEngine
)


def run_decision():

    candidate_data = {

        "candidate_id": "C001",

        "hiring_fit": 84,

        "integrity_score": 82,

        "behavior_score": 78

    }

    decision = DecisionEngine().decide(

        candidate_data["hiring_fit"],

        candidate_data["integrity_score"],

        candidate_data["behavior_score"]

    )

    confidence = (

        ConfidenceCalculator.calculate(

            candidate_data["hiring_fit"],

            candidate_data["integrity_score"],

            candidate_data["behavior_score"]

        )

    )

    risks = RiskAnalyzer.analyze(

        candidate_data["integrity_score"],

        candidate_data["behavior_score"]

    )

    result = {

        "candidate_id":
        candidate_data["candidate_id"],

        "decision":
        decision,

        "confidence_score":
        confidence,

        "risk_factors":
        risks,

        "recommendation":
        RecommendationEngine.generate(
            decision
        ),

        "explanation": {

            "hiring_fit":
            candidate_data["hiring_fit"],

            "integrity_score":
            candidate_data["integrity_score"],

            "behavior_score":
            candidate_data["behavior_score"]
        }
    }

    os.makedirs(
        "output/final_decisions",
        exist_ok=True
    )

    with open(
        "output/final_decisions/candidate_decision.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4
        )

    print(
        "Decision Generated Successfully"
    )


if __name__ == "__main__":

    run_decision()