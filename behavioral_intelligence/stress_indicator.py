class StressIndicator:
    """
    Estimates stress level using
    confidence and sentiment.
    """

    @staticmethod
    def analyze(

        confidence_result,

        sentiment_result

    ):

        stress = 0

        stress += (

            confidence_result[

                "hesitation_count"

            ] * 10

        )

        stress += (

            confidence_result[

                "repeated_words"

            ] * 5

        )

        if (

            sentiment_result[

                "sentiment"

            ] == "Negative"

        ):

            stress += 20

        stress = min(

            stress,

            100

        )

        return {

            "stress_score": stress

        }


if __name__ == "__main__":

    confidence = {

        "hesitation_count": 2,

        "repeated_words": 1

    }

    sentiment = {

        "sentiment": "Negative"

    }

    print(

        StressIndicator.analyze(

            confidence,

            sentiment

        )

    )