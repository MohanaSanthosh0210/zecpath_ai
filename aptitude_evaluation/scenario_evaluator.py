class ScenarioEvaluator:
    """
    Evaluates how well the candidate answered
    the selected reasoning scenario.
    """

    @staticmethod
    def evaluate(answer_text, expected_keywords):

        answer = (answer_text or "").lower()

        matched = []
        missing = []

        for keyword in expected_keywords:
            if keyword.lower() in answer:
                matched.append(keyword)
            else:
                missing.append(keyword)

        coverage = round(
            (len(matched) / len(expected_keywords)) * 100,
            2
        ) if expected_keywords else 0

        context_terms = [
            "impact",
            "team",
            "manager",
            "plan",
            "communicate",
            "priority",
            "deadline",
            "problem"
        ]

        context_hits = [term for term in context_terms if term in answer]
        context_bonus = min(len(context_hits) * 5, 20)

        return {
            "scenario_score": round(min(100, coverage + context_bonus), 2),
            "matched_keywords": matched,
            "missing_keywords": missing,
            "context_terms": context_hits
        }


if __name__ == "__main__":

    answer = (

        "I would prioritize the tasks "

        "and communicate with my manager."

    )

    expected = [

        "prioritize",

        "impact",

        "communicate",

        "plan"

    ]

    print(

        ScenarioEvaluator.evaluate(

            answer,

            expected

        )

    )