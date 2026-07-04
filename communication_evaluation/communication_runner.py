import json
import os

from communication_evaluation.communication_scorer import (
    CommunicationScorer
)


INPUT_FILE = (
    "data/understood_answers/sample_answer.json"
)


def load_candidate_answer():

    if not os.path.exists(INPUT_FILE):

        raise FileNotFoundError(

            f"{INPUT_FILE} not found."

        )

    with open(

        INPUT_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        data = json.load(file)

    # -----------------------------------------
    # Read Day 25 output
    # -----------------------------------------

    try:

        return data["structured_answer"]["text"]

    except KeyError:

        raise ValueError(

            "structured_answer.text not found in "

            "sample_answer.json"

        )


def main():

    answer = load_candidate_answer()

    scorer = CommunicationScorer()

    result = scorer.calculate(

        answer

    )

    print(

        "\n========== COMMUNICATION SCORE ==========\n"

    )

    print(

        json.dumps(

            result,

            indent=4

        )

    )

    print(

        "\nCommunication report saved to "

        "data/communication/communication_score.json"

    )


if __name__ == "__main__":

    main()