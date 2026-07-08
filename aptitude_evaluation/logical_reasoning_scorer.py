class LogicalReasoningScorer:
    """
    Scores reasoning quality using
    a blend of expected keywords and
    evidence of structured thinking.
    """

    @staticmethod
    def calculate(answer_text, expected_keywords):

        answer = (answer_text or "").lower()

        matched = 0
        detected = []

        for keyword in expected_keywords:
            if keyword.lower() in answer:
                matched += 1
                detected.append(keyword)

        support_terms = [
            "reasoning",
            "because",
            "therefore",
            "first",
            "then",
            "step",
            "approach",
            "understand",
            "evaluate"
        ]

        support_hits = [
            term for term in support_terms if term in answer
        ]

        if len(expected_keywords) == 0:
            score = 0
        else:
            keyword_score = (matched / len(expected_keywords)) * 100
            support_bonus = min(len(support_hits) * 8, 24)
            score = round(min(100, keyword_score + support_bonus), 2)

        return {
            "logical_reasoning_score": score,
            "matched_keywords": detected,
            "supporting_terms": support_hits,
            "total_keywords": len(expected_keywords)
        }


if __name__ == "__main__":

    sample_answer = (

        "I would communicate with the teammate, "

        "understand the issue and help fix it "

        "before informing the manager."

    )

    keywords = [

        "communicate",

        "understand",

        "help",

        "manager"

    ]

    print(

        LogicalReasoningScorer.calculate(

            sample_answer,

            keywords

        )

    )