class HesitationDetector:

    HESITATION_WORDS = [
        "um",
        "uh",
        "hmm",
        "erm"
    ]

    @classmethod
    def detect(cls, text):

        text = text.lower()

        count = 0

        for word in cls.HESITATION_WORDS:
            count += text.count(word)

        return count