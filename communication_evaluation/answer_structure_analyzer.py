class AnswerStructureAnalyzer:
    """
    Evaluates answer organization.

    Checks whether the answer contains:

    • Introduction
    • Supporting explanation
    • Closing statement

    Unlike the previous version,
    it does not rely only on keywords.
    """

    INTRO_WORDS = [

        "first",

        "initially",

        "to begin",

        "my experience",

        "i have",

        "i am",

        "i worked",

        "my project"

    ]

    BODY_WORDS = [

        "then",

        "after",

        "because",

        "during",

        "also",

        "worked",

        "developed",

        "implemented",

        "built",

        "created"

    ]

    CONCLUSION_WORDS = [

        "finally",

        "overall",

        "therefore",

        "in conclusion",

        "as a result",

        "successfully"

    ]

    @classmethod
    def analyze(cls, answer):

        text = answer.lower()

        sentences = [

            s.strip()

            for s in text.replace("!", ".").replace("?", ".").split(".")

            if s.strip()

        ]

        introduction = False

        body = False

        conclusion = False

        # ------------------------
        # Introduction
        # ------------------------

        if sentences:

            first_sentence = sentences[0]

            for word in cls.INTRO_WORDS:

                if word in first_sentence:

                    introduction = True

                    break

        # ------------------------
        # Body
        # ------------------------

        if len(sentences) >= 2:

            body = True

        else:

            for word in cls.BODY_WORDS:

                if word in text:

                    body = True

                    break

        # ------------------------
        # Conclusion
        # ------------------------

        if len(sentences) >= 3:

            last_sentence = sentences[-1]

            for word in cls.CONCLUSION_WORDS:

                if word in last_sentence:

                    conclusion = True

                    break

        score = 0

        if introduction:

            score += 35

        if body:

            score += 35

        if conclusion:

            score += 30

        # Two well-organized sentences deserve partial credit

        if (

            len(sentences) >= 2

            and

            score < 70

        ):

            score = 70

        return {

            "structure_score": score,

            "introduction": introduction,

            "body": body,

            "conclusion": conclusion,

            "sentence_count": len(sentences)

        }


if __name__ == "__main__":

    sample = (

        "I have two years of experience in Python. "

        "I worked on Flask and Django projects."

    )

    print(

        AnswerStructureAnalyzer.analyze(

            sample

        )

    )