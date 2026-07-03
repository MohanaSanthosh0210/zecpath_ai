class VagueAnswerDetector:

    """
    Detects whether a candidate response is
    vague or incomplete.
    """

    VAGUE_PHRASES = [

        "i don't know",

        "not sure",

        "maybe",

        "i guess",

        "something like",

        "etc",

        "whatever",

        "nothing much",

        "can't remember"

    ]

    MINIMUM_WORDS = 6

    @classmethod
    def analyze(cls, answer):

        answer = answer.lower().strip()

        words = answer.split()

        is_short = len(words) < cls.MINIMUM_WORDS

        vague_phrases = []

        for phrase in cls.VAGUE_PHRASES:

            if phrase in answer:

                vague_phrases.append(phrase)

        return {

            "is_vague":

                len(vague_phrases) > 0,

            "is_incomplete":

                is_short,

            "matched_phrases":

                vague_phrases,

            "word_count":

                len(words)

        }


if __name__ == "__main__":

    answer = "Maybe I worked on Python."

    result = VagueAnswerDetector.analyze(

        answer

    )

    print(result)