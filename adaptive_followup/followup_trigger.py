from adaptive_followup.vague_answer_detector import (

    VagueAnswerDetector

)


class FollowUpTrigger:

    """
    Generates the appropriate follow-up
    question based on candidate response.
    """

    @staticmethod
    def generate(

        original_question,

        answer

    ):

        analysis = (

            VagueAnswerDetector.analyze(

                answer

            )

        )

        if analysis["is_incomplete"]:
            return {
                "trigger": "Clarification",
                "follow_up": "Could you explain your answer in a little more detail?",
            }

        if analysis["is_vague"]:
            return {
                "trigger": "Clarification",
                "follow_up": "Could you clarify what you mean?",
            }

        if analysis["word_count"] <= 12:
            return {
                "trigger": "Deepening",
                "follow_up": "Can you tell me more about your experience?",
            }

        return {
            "trigger": "Example",
            "follow_up": "Could you provide a real example from your experience?",
        }


if __name__ == "__main__":

    question = "Tell me about your teamwork experience."

    answer = "I worked in a team."

    decision = FollowUpTrigger.generate(

        question,

        answer

    )

    print("\n===== FOLLOW-UP DECISION =====\n")

    print(decision)