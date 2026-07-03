class RepetitionDetector:

    """
    Prevents asking the same follow-up
    repeatedly.
    """

    def __init__(self):

        self.previous_questions = []

    def already_asked(

        self,

        question

    ):

        return (

            question.lower()

            in

            [

                q.lower()

                for q

                in self.previous_questions

            ]

        )

    def add_question(

        self,

        question

    ):

        if not self.already_asked(

            question

        ):

            self.previous_questions.append(

                question

            )

    def suggest(

        self,

        follow_up

    ):

        if self.already_asked(

            follow_up

        ):

            return {

                "allowed": False,

                "reason":

                    "Question already asked.",

                "alternative":

                    "Let's move to the next topic."

            }

        self.add_question(

            follow_up

        )

        return {

            "allowed": True,

            "question":

                follow_up

        }


if __name__ == "__main__":

    detector = RepetitionDetector()

    print(

        detector.suggest(

            "Could you explain further?"

        )

    )

    print(

        detector.suggest(

            "Could you explain further?"

        )

    )

    print(

        detector.suggest(

            "Can you give an example?"

        )

    )