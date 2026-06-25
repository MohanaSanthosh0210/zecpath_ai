class UncertaintyDetector:

    UNCERTAINTY_WORDS = [
        "maybe",
        "probably",
        "perhaps",
        "not sure",
        "i think",
        "might"
    ]

    @classmethod
    def detect(cls, text):

        text = text.lower()

        count = 0

        for word in cls.UNCERTAINTY_WORDS:
            count += text.count(word)

        return count