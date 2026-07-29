class SummaryGenerator:

    @staticmethod
    def generate(profile):

        hiring_fit = (

            profile

            .get(
                "overall_score",
                {}
            )

            .get(
                "hiring_fit",
                0
            )

        )

        decision = (

            profile

            .get(
                "final_decision",
                {}
            )

            .get(
                "decision",
                "UNKNOWN"
            )

        )

        summary = {

            "executive_summary":

                (

                    "Candidate has completed all "

                    "evaluation stages successfully. "

                    f"Overall Hiring Fit: "

                    f"{hiring_fit}%. "

                    f"Final Recommendation: "

                    f"{decision}."

                )

        }

        return summary


if __name__ == "__main__":

    sample = {

        "overall_score": {

            "hiring_fit": 88

        },

        "final_decision": {

            "decision": "Selected"

        }

    }

    print(

        SummaryGenerator.generate(sample)

    )