from dataclasses import dataclass, field


@dataclass
class ConversationContext:

    candidate_id: str = "unknown"

    job_id: str = "unknown"

    current_question_index: int = 0

    retry_count: int = 0

    silence_count: int = 0

    followup_count: int = 0

    conversation_state: str = "START"

    interview_finished: bool = False

    previous_answer: str = ""

    conversation_history: list = field(default_factory=list)

    def add_history(
        self,
        question,
        answer
    ):

        self.conversation_history.append({

            "question": question,

            "answer": answer
        })