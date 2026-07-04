class VocabularyAnalyzer:
    """
    Estimates vocabulary richness using
    unique word ratio.
    """

    @classmethod
    def analyze(cls, answer):

        words = [

            word.lower().strip(".,!?")

            for word in answer.split()

            if word.strip()

        ]

        total_words = len(words)

        unique_words = len(set(words))

        if total_words == 0:

            ratio = 0

        else:

            ratio = unique_words / total_words

        score = min(

            100,

            int(ratio * 120)

        )

        return {

            "vocabulary_score": score,

            "total_words": total_words,

            "unique_words": unique_words,

            "vocabulary_ratio":

                round(

                    ratio,

                    2

                )

        }