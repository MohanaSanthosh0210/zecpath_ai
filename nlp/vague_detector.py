class VagueDetector:

    VAGUE_WORDS = [

        "some",
        "many",
        "few",
        "good",
        "okay",
        "etc"
    ]

    @staticmethod
    def detect(answer):

        answer = answer.lower()

        for word in VagueDetector.VAGUE_WORDS:

            if word in answer:
                return True

        return False