class SentimentScorer:

    POSITIVE_WORDS = [

        "confident",
        "excellent",
        "strong",
        "successful",
        "achieved",
        "developed",
        "improved",
        "completed"
    ]

    NEGATIVE_WORDS = [

        "difficult",
        "problem",
        "failed",
        "weak",
        "struggle",
        "confused"
    ]

    @classmethod
    def score(cls, text):

        text = text.lower()

        positive = 0
        negative = 0

        for word in cls.POSITIVE_WORDS:

            if word in text:
                positive += 1

        for word in cls.NEGATIVE_WORDS:

            if word in text:
                negative += 1

        sentiment_score = (
            positive - negative
        )

        if sentiment_score > 0:

            sentiment = "Positive"

        elif sentiment_score < 0:

            sentiment = "Negative"

        else:

            sentiment = "Neutral"

        return {

            "sentiment":
                sentiment,

            "positive_signals":
                positive,

            "negative_signals":
                negative,

            "sentiment_score":
                sentiment_score
        }