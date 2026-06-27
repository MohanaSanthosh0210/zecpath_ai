class FollowUpEngine:
    """
    Generates follow-up questions when the AI
    determines that an answer is incomplete,
    vague, or off-topic.
    """

    FOLLOW_UPS = {

        "experience_information":
            "Can you explain one of the projects where you used this technology?",

        "skill_information":
            "Can you describe how you have used this skill in a real project?",

        "project_information":
            "What was your exact role in that project?",

        "salary_information":
            "Could you specify your expected annual salary?",

        "availability_information":
            "When would you be able to join the company?",

        "education_information":
            "Could you tell me more about your educational background?"
    }

    DEFAULT_QUESTION = (
        "Could you please provide more details?"
    )

    @classmethod
    def generate(
        cls,
        understood_answer
    ):

        intent = understood_answer.get(
            "intent",
            "unknown"
        )

        return cls.FOLLOW_UPS.get(

            intent,

            cls.DEFAULT_QUESTION

        )