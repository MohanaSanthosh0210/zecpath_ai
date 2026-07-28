class RiskAnalyzer:

    @staticmethod
    def analyze(

        integrity_score,

        behavior_score

    ):

        risks = []

        if integrity_score < 60:

            risks.append(
                "Integrity Risk"
            )

        if behavior_score < 60:

            risks.append(
                "Behavior Risk"
            )

        if not risks:

            risks.append(
                "No Major Risks"
            )

        return risks