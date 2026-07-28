class RecommendationEngine:

    @staticmethod
    def generate(
        decision
    ):

        if decision == "Selected":

            return (
                "Proceed with hiring."
            )

        if decision == "Hold / Review":

            return (
                "Requires recruiter review."
            )

        return (
            "Candidate rejected."
        )