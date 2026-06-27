from conversation.conversation_state_machine import (
    ConversationState
)


class SilenceHandler:

    MAX_SILENCE = 2

    @classmethod
    def handle(cls, context):

        context.silence_count += 1

        if context.silence_count >= cls.MAX_SILENCE:

            context.interview_finished = True

            context.conversation_state = (
                ConversationState.END.value
            )

            return {

                "state":
                    ConversationState.END.value,

                "message":
                    "The interview has been ended because no response was received after multiple attempts."
            }

        context.conversation_state = (
            ConversationState.RETRY.value
        )

        return {

            "state":
                ConversationState.RETRY.value,

            "message":
                "Sorry, I couldn't hear you. Could you please repeat your answer?"
        }