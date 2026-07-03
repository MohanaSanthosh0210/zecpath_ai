class ConversationTracker:

    """
    Tracks conversation history and previously
    asked follow-up questions.
    """

    def __init__(self):

        self.history = []

    def add(

        self,

        question,

        answer

    ):

        self.history.append({

            "question": question,

            "answer": answer

        })

    def get_history(self):

        return self.history

    def total_questions(self):

        return len(self.history)

    def last_question(self):

        if not self.history:

            return None

        return self.history[-1]