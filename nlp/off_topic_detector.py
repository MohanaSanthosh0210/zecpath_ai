class OffTopicDetector:

    @staticmethod
    def detect(question, answer):

        question_words = set(
            question.lower().split()
        )

        answer_words = set(
            answer.lower().split()
        )

        overlap = (
            question_words
            .intersection(answer_words)
        )

        return len(overlap) == 0