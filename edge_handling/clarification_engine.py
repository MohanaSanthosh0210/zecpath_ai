class ClarificationEngine:

    CLARIFICATION_MESSAGES = {

        "poor_audio":
            "I'm sorry, your audio wasn't clear. Could you please repeat your answer?",

        "language_mix":
            "Could you please answer in one language so I can understand better?",

        "missing_answer":
            "I couldn't understand your response. Could you answer the question again?",

        "background_noise":
            "There seems to be background noise. Could you move to a quieter place and repeat your answer?"
    }

    @classmethod
    def get_message(cls, issue):

        return cls.CLARIFICATION_MESSAGES.get(

            issue,

            "Could you please clarify your answer?"

        )