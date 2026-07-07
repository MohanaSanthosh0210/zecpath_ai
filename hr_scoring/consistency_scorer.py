class ConsistencyScorer:
    """
    Computes consistency using the
    structured answer generated in Day 25.
    """

    @staticmethod
    def calculate(answer_json):

        score = 100

        reasons = []

        if answer_json.get(

            "vague_response",

            False

        ):

            score -= 20

            reasons.append(

                "Vague response"

            )

        if answer_json.get(

            "missing_details",

            False

        ):

            score -= 15

            reasons.append(

                "Missing details"

            )

        if answer_json.get(

            "off_topic",

            False

        ):

            score -= 30

            reasons.append(

                "Off-topic response"

            )

        score = max(0, score)

        return {

            "consistency_score": score,

            "reasons": reasons

        }


if __name__ == "__main__":

    sample = {

        "off_topic": False,

        "missing_details": False,

        "vague_response": False

    }

    print(

        ConsistencyScorer.calculate(

            sample

        )

    )