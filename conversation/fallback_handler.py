from conversation.conversation_state_machine import (
    ConversationState
)


class FallbackHandler:

    FALLBACK_QUESTIONS = {

        "experience_information":
            "Could you describe one project where you applied your experience?",

        "skill_information":
            "Could you explain how you have used this skill in practice?",

        "project_information":
            "Can you tell me more about your responsibilities in that project?",

        "salary_information":
            "Could you specify your expected salary package?",

        "availability_information":
            "When will you be available to join?",

        "education_information":
            "Could you tell me more about your educational background?"
    }

    DEFAULT_FALLBACK = (
        "Could you please explain your answer in a different way?"
    )

    @classmethod
    def handle(

        cls,

        context,

        intent="unknown"

    ):

        context.conversation_state = (
            ConversationState.FOLLOW_UP.value
        )

        return {

            "state":
                ConversationState.FOLLOW_UP.value,

            "question":
                cls.FALLBACK_QUESTIONS.get(

                    intent,

                    cls.DEFAULT_FALLBACK
                )
        }