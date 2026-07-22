class ReasoningScorer:

    @staticmethod
    def score(answer_data):

        score = answer_data.get(
            "reasoning_score",
            0
        )

        return {

            "reasoning": float(score)

        }


if __name__ == "__main__":

    sample = {

        "reasoning_score": 90

    }

    print(

        ReasoningScorer.score(sample)

    )