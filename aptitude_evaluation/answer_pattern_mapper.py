class AnswerPatternMapper:
    """
    Maps the candidate answer into an
    explainable reasoning structure.
    """

    @staticmethod
    def map(answer_text):

        answer = answer_text.lower()

        pattern = {

            "identified_problem": False,

            "explained_reasoning": False,

            "proposed_solution": False,

            "mentioned_result": False

        }

        if any(

            word in answer

            for word in

            [

                "problem",

                "issue",

                "challenge"

            ]

        ):

            pattern["identified_problem"] = True

        if any(

            word in answer

            for word in

            [

                "because",

                "therefore",

                "reason"

            ]

        ):

            pattern["explained_reasoning"] = True

        if any(

            word in answer

            for word in

            [

                "solution",

                "fix",

                "resolve",

                "implement"

            ]

        ):

            pattern["proposed_solution"] = True

        if any(

            word in answer

            for word in

            [

                "result",

                "outcome",

                "improved",

                "success"

            ]

        ):

            pattern["mentioned_result"] = True

        score = (

            sum(pattern.values())

            /

            4

        ) * 100

        return {

            "answer_pattern_score": round(score, 2),

            "pattern": pattern

        }


if __name__ == "__main__":

    sample = (

        "The problem was a deployment issue "

        "because the configuration failed. "

        "I implemented a solution "

        "and the result was successful."

    )

    print(

        AnswerPatternMapper.map(

            sample

        )

    )