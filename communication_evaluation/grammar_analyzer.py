class GrammarAnalyzer:
    """
    Basic grammar quality estimator.
    """

    @classmethod
    def analyze(cls, answer):

        score = 100

        issues = []

        answer = answer.strip()

        if answer:

            if answer[0].islower():

                score -= 10

                issues.append(

                    "Sentence should start with a capital letter."

                )

            if answer[-1] not in ".!?":

                score -= 10

                issues.append(

                    "Sentence should end with punctuation."

                )

        double_spaces = answer.count("  ")

        if double_spaces:

            score -= double_spaces * 2

            issues.append(

                "Multiple consecutive spaces detected."

            )

        score = max(0, score)

        return {

            "grammar_score": score,

            "issues": issues

        }