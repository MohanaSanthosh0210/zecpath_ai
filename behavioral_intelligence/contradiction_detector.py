class ContradictionDetector:
    """
    Detects contradictions using
    structured Day 25 outputs.
    """

    @staticmethod
    def detect(answer_json):

        contradictions = []

        text = (

            answer_json

            .get(

                "structured_answer",

                {}

            )

            .get(

                "text",

                ""

            )

            .lower()

        )

        experience = (

            answer_json.get(

                "experience"

            )

        )

        availability = (

            answer_json.get(

                "availability"

            )

        )

        salary = (

            answer_json.get(

                "salary_expectation"

            )

        )

        if (

            experience

            and

            "no experience" in text

        ):

            contradictions.append(

                "Experience conflict detected"

            )

        if (

            availability

            and

            "not available" in text

        ):

            contradictions.append(

                "Availability conflict detected"

            )

        if (

            salary

            and

            "no salary expectation" in text

        ):

            contradictions.append(

                "Salary conflict detected"

            )

        contradiction_score = max(

            0,

            100 - (

                len(

                    contradictions

                ) * 25

            )

        )

        return {

            "contradictions": contradictions,

            "count": len(

                contradictions

            ),

            "contradiction_score":

                contradiction_score

        }


if __name__ == "__main__":

    sample = {

        "experience": "2 years",

        "structured_answer": {

            "text":

            "I have no experience."

        }

    }

    print(

        ContradictionDetector.detect(

            sample

        )

    )