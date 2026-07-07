class RelevanceScorer:
    """
    Calculates answer relevance using
    Day 25 Answer Understanding output.
    """

    @staticmethod
    def calculate(answer_json):

        score = 100

        deductions = []

        if answer_json.get(

            "off_topic",

            False

        ):

            score -= 40

            deductions.append(

                "Off-topic response"

            )

        if answer_json.get(

            "missing_details",

            False

        ):

            score -= 20

            deductions.append(

                "Missing important details"

            )

        if answer_json.get(

            "vague_response",

            False

        ):

            score -= 20

            deductions.append(

                "Vague answer"

            )

        confidence = (

            answer_json.get(

                "structured_answer",

                {}

            ).get(

                "intent_confidence",

                answer_json.get(

                    "confidence",

                    0.50

                )

            )

        )

        if confidence < 0.50:

            score -= 10

            deductions.append(

                "Low intent confidence"

            )

        score = max(0, score)

        return {

            "relevance_score": score,

            "intent_confidence": confidence,

            "deductions": deductions

        }


if __name__ == "__main__":

    sample = {

        "off_topic": False,

        "missing_details": False,

        "vague_response": False,

        "structured_answer": {

            "intent_confidence": 0.82

        }

    }

    print(

        RelevanceScorer.calculate(

            sample

        )

    )