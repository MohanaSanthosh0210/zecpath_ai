from conversation.conversation_state_machine import (
    ConversationState
)


class RetryHandler:

    MAX_RETRIES = 2

    @classmethod
    def handle(cls, context):

        context.retry_count += 1

        if context.retry_count > cls.MAX_RETRIES:

            context.conversation_state = (
                ConversationState.FOLLOW_UP.value
            )

            return {

                "state":
                    ConversationState.FOLLOW_UP.value,

                "message":
                    "Let's move on. I'll ask the question differently."
            }

        context.conversation_state = (
            ConversationState.RETRY.value
        )

        return {

            "state":
                ConversationState.RETRY.value,

            "message":
                "I'm sorry, I didn't completely understand your answer. Could you repeat it?"
        }