import re


class LanguageMixDetector:

    COMMON_MALAYALAM = [

        "alle",

        "aano",

        "entha",

        "pakshe",

        "njan",

        "cheythu",

        "illa",

        "undu"

    ]

    @classmethod
    def detect(cls, transcript):

        text = transcript.lower()

        english_words = re.findall(

            r"[a-zA-Z]+",

            transcript

        )

        malayalam_hits = 0

        for word in cls.COMMON_MALAYALAM:

            if word in text:

                malayalam_hits += 1

        mixed = (

            len(english_words) > 0

            and

            malayalam_hits > 0

        )

        return {

            "language_mix": mixed,

            "malayalam_words_detected":

                malayalam_hits

        }