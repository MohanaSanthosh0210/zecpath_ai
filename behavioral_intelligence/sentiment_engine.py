class SentimentEngine:
    """
    Performs rule-based sentiment analysis.
    """

    POSITIVE = [

        "achieved",

        "improved",

        "developed",

        "built",

        "implemented",

        "completed",

        "success",

        "successful",

        "confident",

        "learned",

        "managed",

        "delivered"

    ]

    NEGATIVE = [

        "failed",

        "failure",

        "problem",

        "difficult",

        "stress",

        "stressed",

        "confused",

        "unable",

        "worried",

        "panic",

        "hard"

    ]

    @staticmethod
    def analyze(answer: str):

        answer = answer.lower()

        positive = sum(

            answer.count(word)

            for word in SentimentEngine.POSITIVE

        )

        negative = sum(

            answer.count(word)

            for word in SentimentEngine.NEGATIVE

        )

        sentiment_score = 50

        sentiment_score += positive * 10

        sentiment_score -= negative * 10

        sentiment_score = max(

            0,

            min(

                sentiment_score,

                100

            )

        )

        if sentiment_score >= 70:

            label = "Positive"

        elif sentiment_score >= 40:

            label = "Neutral"

        else:

            label = "Negative"

        return {

            "positive_signals": positive,

            "negative_signals": negative,

            "sentiment_score": sentiment_score,

            "sentiment": label

        }


if __name__ == "__main__":

    sample = (

        "I successfully developed "

        "a Django application."

    )

    print(

        SentimentEngine.analyze(

            sample

        )

    )