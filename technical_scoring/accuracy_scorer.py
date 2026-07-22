class AccuracyScorer:

    @staticmethod
    def score(answer_data):

        score = answer_data.get(
            "accuracy_score",
            0
        )

        return {

            "accuracy": float(score)

        }


if __name__ == "__main__":

    sample = {

        "accuracy_score": 88

    }

    print(

        AccuracyScorer.score(sample)

    )