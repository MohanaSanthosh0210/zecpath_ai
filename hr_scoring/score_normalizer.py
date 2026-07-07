class ScoreNormalizer:
    """
    Normalizes interview scores across
    different interview lengths.
    """

    @staticmethod
    def normalize(
        total_score,
        question_count
    ):

        if question_count <= 0:
            return 0

        return round(
            total_score /
            question_count,
            2
        )