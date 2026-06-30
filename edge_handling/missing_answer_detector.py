class MissingAnswerDetector:

    EMPTY_RESPONSES = [

        "",

        "no",

        "none",

        "don't know",

        "do not know",

        "skip",

        "na",

        "n/a"

    ]

    @classmethod
    def detect(cls, transcript):

        if transcript is None:

            return True

        answer = transcript.lower().strip()

        if answer in cls.EMPTY_RESPONSES:

            return True

        if len(answer.split()) < 3:

            return True

        return False