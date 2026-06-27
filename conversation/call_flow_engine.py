import json
import os

from conversation.conversation_state_machine import (
    ConversationState
)

from conversation.followup_engine import (
    FollowUpEngine
)

from conversation.silence_handler import (
    SilenceHandler
)

from conversation.retry_handler import (
    RetryHandler
)

from conversation.fallback_handler import (
    FallbackHandler
)

from conversation.conversation_context import (
    ConversationContext
)


class CallFlowEngine:

    def __init__(self):

        self.context = ConversationContext()

    # ----------------------------------------------------
    # Utility
    # ----------------------------------------------------

    def load_json(self, path):

        if not os.path.exists(path):

            raise FileNotFoundError(
                f"{path} not found."
            )

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    # ----------------------------------------------------
    # Main Decision Engine
    # ----------------------------------------------------

    def next_action(

        self,

        understood_answer,

        behavior_report,

        screening_score

    ):

        # -------------------------
        # Silence
        # -------------------------

        if understood_answer is None:

            return SilenceHandler.handle(

                self.context

            )

        confidence = (

            behavior_report

            .get("confidence", {})

            .get("confidence_score", 0)

        )

        final_score = screening_score.get(

            "final_screening_score",

            0

        )

        intent = understood_answer.get(

            "intent",

            "unknown"

        )

        # -------------------------
        # Missing Details
        # -------------------------

        if understood_answer.get(

            "missing_details",

            False

        ):

            return {

                "state":

                    ConversationState.FOLLOW_UP.value,

                "question":

                    FollowUpEngine.generate(

                        understood_answer

                    )

            }

        # -------------------------
        # Vague
        # -------------------------

        if understood_answer.get(

            "vague_response",

            False

        ):

            return {

                "state":

                    ConversationState.FOLLOW_UP.value,

                "question":

                    "Could you explain that in more detail?"

            }

        # -------------------------
        # Low Confidence
        # -------------------------

        if confidence < 60:

            return RetryHandler.handle(

                self.context

            )

        # -------------------------
        # Low Screening Score
        # -------------------------

        if final_score < 60:

            return FallbackHandler.handle(

                self.context,

                intent

            )

        # -------------------------
        # Off Topic
        # -------------------------

        if understood_answer.get(

            "off_topic",

            False

        ):

            return {

                "state":

                    ConversationState.FOLLOW_UP.value,

                "question":

                    "Could you answer the question more specifically?"

            }

        # -------------------------
        # Good Answer
        # -------------------------

        self.context.current_question_index += 1

        self.context.conversation_state = (

            ConversationState.NEXT_QUESTION.value

        )

        return {

            "state":

                ConversationState.NEXT_QUESTION.value,

            "message":

                "Proceed to the next interview question."

        }

    # ----------------------------------------------------
    # Complete Pipeline
    # ----------------------------------------------------

    def run(self):

        understood_answer = self.load_json(
            "data/understood_answers/sample_answer.json"
        )

        behavior_report = self.load_json(
            "data/behavioral_reports/sample_answer.json"
        )

        screening_score = self.load_json(
            "data/screening_scores/final_scores/unknown.json"
        )

        result = self.next_action(
            understood_answer,
            behavior_report,
            screening_score
        )

        # -----------------------------
        # Save Result
        # -----------------------------

        os.makedirs(
            "data/conversation_flow",
            exist_ok=True
        )

        print("\n===== DEBUG RESULT =====")
        print(result)
        print(type(result))

        output_file = "data/conversation_flow/conversation_decision.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )

        print("\n===== AI Conversation Decision =====\n")

        print(
            json.dumps(
                result,
                indent=4
            )
        )

        print(f"\nConversation decision saved successfully.")

        print(f"Saved to: {os.path.abspath(output_file)}")


if __name__ == "__main__":

    engine = CallFlowEngine()

    engine.run()