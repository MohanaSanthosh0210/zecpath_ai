from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class InterviewState:

    """
    Maintains the complete interview state.
    """

    candidate_id: str = "UNKNOWN"

    current_phase: str = "INTRODUCTION"

    current_question_id: str = ""

    current_question: str = ""

    response: str = ""

    follow_up_required: bool = False

    interview_completed: bool = False

    conversation_history: List[Dict] = field(default_factory=list)

    def update(

        self,

        question_id,

        question,

        response,

        follow_up=False

    ):

        self.current_question_id = question_id

        self.current_question = question

        self.response = response

        self.follow_up_required = follow_up

        self.conversation_history.append({

            "question_id": question_id,

            "question": question,

            "response": response,

            "follow_up_required": follow_up

        })

    def next_phase(

        self,

        phase

    ):

        self.current_phase = phase

    def end_interview(self):

        self.interview_completed = True

    def to_dict(self):

        return {

            "candidate_id":

                self.candidate_id,

            "current_phase":

                self.current_phase,

            "current_question_id":

                self.current_question_id,

            "current_question":

                self.current_question,

            "response":

                self.response,

            "follow_up_required":

                self.follow_up_required,

            "interview_completed":

                self.interview_completed,

            "conversation_history":

                self.conversation_history

        }