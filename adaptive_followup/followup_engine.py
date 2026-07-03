import json
import os

from adaptive_followup.followup_trigger import (
    FollowUpTrigger
)

from adaptive_followup.difficulty_adapter import (
    DifficultyAdapter
)

from adaptive_followup.repetition_detector import (
    RepetitionDetector
)

from adaptive_followup.conversation_tracker import (
    ConversationTracker
)


class FollowUpEngine:

    OUTPUT_FILE = (
        "data/adaptive_followup/followup_decision.json"
    )

    def __init__(self):

        self.repetition = RepetitionDetector()

        self.tracker = ConversationTracker()

    def decide(

        self,

        question,

        answer,

        confidence_score=75

    ):

        trigger = FollowUpTrigger.generate(

            question,

            answer

        )

        difficulty = DifficultyAdapter.adapt(

            answer,

            confidence_score

        )

        repetition = self.repetition.suggest(

            trigger["follow_up"]

        )

        self.tracker.add(

            question,

            answer

        )

        decision = {

            "current_question":

                question,

            "candidate_answer":

                answer,

            "trigger":

                trigger,

            "difficulty":

                difficulty,

            "repetition":

                repetition,

            "conversation": {

                "questions_asked":

                    self.tracker.total_questions(),

                "history":

                    self.tracker.get_history()

            }

        }

        os.makedirs(

            "data/adaptive_followup",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                decision,

                file,

                indent=4

            )

        return decision