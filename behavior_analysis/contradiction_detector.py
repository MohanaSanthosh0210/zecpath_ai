class ContradictionDetector:

    CONTRADICTION_PAIRS = [

        ("yes", "no"),

        ("experienced", "no experience"),

        ("expert", "beginner"),

        ("immediately", "2 months"),

        ("available", "not available")
    ]

    @classmethod
    def detect(cls, text):

        text = text.lower()

        contradictions = []

        for first, second in cls.CONTRADICTION_PAIRS:

            if first in text and second in text:

                contradictions.append(
                    f"{first} vs {second}"
                )

        return contradictions