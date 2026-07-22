class ApplicabilityScorer:

    @staticmethod
    def score(answer_data):

        score = answer_data.get(
            "applicability_score",
            0
        )

        return {

            "applicability": float(score)

        }


if __name__ == "__main__":

    sample = {

        "applicability_score": 80

    }

    print(

        ApplicabilityScorer.score(sample)

    )