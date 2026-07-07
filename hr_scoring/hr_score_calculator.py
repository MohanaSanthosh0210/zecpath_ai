class HRScoreCalculator:
    """
    Calculates weighted HR Interview Score.
    """

    @staticmethod
    def calculate(
        relevance,
        communication,
        confidence,
        consistency,
        weights
    ):

        score = (

            relevance *
            weights["relevance"]

            +

            communication *
            weights["communication"]

            +

            confidence *
            weights["confidence"]

            +

            consistency *
            weights["consistency"]

        )

        return round(score, 2)