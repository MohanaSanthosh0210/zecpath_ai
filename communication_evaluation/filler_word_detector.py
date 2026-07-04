class FillerWordDetector:
    """
    Detects filler words and estimates their impact
    on communication quality.
    """

    FILLER_WORDS = [

        "um",

        "uh",

        "hmm",

        "like",

        "you know",

        "actually",

        "basically",

        "literally",

        "kind of",

        "sort of",

        "okay",

        "well"

    ]

    @classmethod
    def analyze(cls, answer):

        answer_lower = answer.lower()

        detected = {}

        total = 0

        for filler in cls.FILLER_WORDS:

            count = answer_lower.count(filler)

            if count > 0:

                detected[filler] = count

                total += count

        score = max(

            0,

            100 - total * 5

        )

        return {

            "filler_score": score,

            "total_fillers": total,

            "detected_fillers": detected

        }


if __name__ == "__main__":

    sample = (

        "Well, actually I kind of worked "

        "on a project, you know."

    )

    print(

        FillerWordDetector.analyze(

            sample

        )

    )