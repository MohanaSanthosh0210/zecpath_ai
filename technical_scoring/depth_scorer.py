class DepthScorer:

    @staticmethod
    def score(answer_data):

        score = answer_data.get(
            "depth_score",
            0
        )

        return {

            "depth": float(score)

        }


if __name__ == "__main__":

    sample = {

        "depth_score": 82

    }

    print(

        DepthScorer.score(sample)

    )