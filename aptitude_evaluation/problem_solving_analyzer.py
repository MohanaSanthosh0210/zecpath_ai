class ProblemSolvingAnalyzer:
    """
    Detects whether the candidate explains
    a structured problem-solving process.
    """

    PROBLEM_SOLVING_KEYWORDS = [
        "analyze",
        "identify",
        "plan",
        "prioritize",
        "implement",
        "solution",
        "evaluate",
        "test",
        "review",
        "confirm",
        "fix",
        "root cause"
    ]

    @staticmethod
    def analyze(answer_text):

        answer = (answer_text or "").lower()

        detected = []

        for keyword in ProblemSolvingAnalyzer.PROBLEM_SOLVING_KEYWORDS:
            if keyword in answer:
                detected.append(keyword)

        if len(detected) == 0:
            score = 0
        else:
            score = round(min(100, (len(detected) / 8) * 100), 2)

        return {
            "problem_solving_score": score,
            "detected_keywords": detected
        }


if __name__ == "__main__":

    sample = (

        "First I analyze the issue, "

        "identify the root cause, "

        "plan a solution "

        "and test it."

    )

    print(

        ProblemSolvingAnalyzer.analyze(

            sample

        )

    )