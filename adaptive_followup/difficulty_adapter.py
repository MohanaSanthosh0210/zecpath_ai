class DifficultyAdapter:

    """
    Adjusts follow-up difficulty based on
    candidate response quality.
    """

    SIMPLE_THRESHOLD = 8
    CONFIDENT_THRESHOLD = 20

    @classmethod
    def adapt(

        cls,

        answer,

        confidence_score=70

    ):

        word_count = len(

            answer.split()

        )

        # -----------------------------
        # Very Short Answer
        # -----------------------------

        if word_count < cls.SIMPLE_THRESHOLD:

            return {

                "difficulty":

                    "Simple",

                "follow_up_type":

                    "Deepening",

                "question":

                    "Could you explain that in more detail?"

            }

        # -----------------------------
        # Good Answer
        # -----------------------------

        if (

            confidence_score >= 80

            and

            word_count >= cls.CONFIDENT_THRESHOLD

        ):

            return {

                "difficulty":

                    "Advanced",

                "follow_up_type":

                    "Scenario",

                "question":

                    "Can you describe a real situation where you applied this?"

            }

        # -----------------------------
        # Medium Quality
        # -----------------------------

        return {

            "difficulty":

                "Medium",

            "follow_up_type":

                "Clarification",

            "question":

                "Could you expand a little more on your answer?"

        }


if __name__ == "__main__":

    response = (

        "I developed APIs using Django and "

        "deployed them on AWS."

    )

    result = DifficultyAdapter.adapt(

        response,

        confidence_score=90

    )

    print(result)