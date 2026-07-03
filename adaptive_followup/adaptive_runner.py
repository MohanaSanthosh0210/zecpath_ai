import json

from adaptive_followup.followup_engine import (
    FollowUpEngine
)


def main():

    engine = FollowUpEngine()

    question = (

        "Tell me about a project you worked on."

    )

    answer = (

        "I developed REST APIs using Django "

        "and deployed them on AWS."

    )

    result = engine.decide(

        question,

        answer,

        confidence_score=90

    )

    print(

        "\n========== FOLLOW-UP DECISION ==========\n"

    )

    print(

        json.dumps(

            result,

            indent=4

        )

    )

    print(

        "\nDecision saved to "

        "data/adaptive_followup/followup_decision.json"

    )


if __name__ == "__main__":

    main()