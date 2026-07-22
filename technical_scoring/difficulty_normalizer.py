class DifficultyNormalizer:

    MULTIPLIERS = {

        "easy": 1.00,

        "medium": 1.05,

        "hard": 1.10,

        "expert": 1.15

    }

    @staticmethod
    def normalize(score, difficulty):

        multiplier = (

            DifficultyNormalizer.MULTIPLIERS.get(

                difficulty.lower(),

                1.0

            )

        )

        normalized = score * multiplier

        return round(

            min(normalized, 100),

            2

        )


if __name__ == "__main__":

    print(

        DifficultyNormalizer.normalize(

            84,

            "hard"

        )

    )