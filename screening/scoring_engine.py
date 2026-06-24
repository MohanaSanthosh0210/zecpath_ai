class ScreeningScoringEngine:

    def __init__(self, weights=None):
        self.weights = weights or {
            "clarity": 0.25,
            "relevance": 0.35,
            "completeness": 0.25,
            "consistency": 0.15
        }

    @staticmethod
    def normalize_score(score):
        return max(0, min(100, round(score, 2)))

    def calculate_clarity(self, answer):
        if not isinstance(answer, str) or not answer.strip():
            return 30

        words = answer.split()
        word_count = len(words)

        if word_count >= 25:
            return 100
        if word_count >= 18:
            return 90
        if word_count >= 12:
            return 80
        if word_count >= 7:
            return 70
        if word_count >= 4:
            return 55

        return 40

    def calculate_relevance(self, answer_data):
        if answer_data.get("off_topic", False):
            return 20

        confidence = float(answer_data.get("confidence", 0.0))

        if confidence >= 0.85:
            return 100
        if confidence >= 0.65:
            return 85
        if confidence >= 0.45:
            return 70

        return 55

    def calculate_completeness(self, answer_data):
        if answer_data.get("missing_details", False):
            return 45

        return 100

    def calculate_consistency(self, answer_data):
        if answer_data.get("vague_response", False):
            return 60

        return 100

    def calculate_final_score(
        self,
        clarity,
        relevance,
        completeness,
        consistency
    ):
        score = (
            clarity * self.weights["clarity"] +
            relevance * self.weights["relevance"] +
            completeness * self.weights["completeness"] +
            consistency * self.weights["consistency"]
        )

        return self.normalize_score(score)

    def score_answer(self, answer_data):
        answer = answer_data.get("answer", "")
        question_id = answer_data.get("question_id") or "unknown"
        candidate_id = answer_data.get("candidate_id") or "unknown"

        clarity = self.calculate_clarity(answer)
        relevance = self.calculate_relevance(answer_data)
        completeness = self.calculate_completeness(answer_data)
        consistency = self.calculate_consistency(answer_data)

        final_score = self.calculate_final_score(
            clarity,
            relevance,
            completeness,
            consistency
        )

        explanation = []

        if clarity >= 90:
            explanation.append("Answer length and structure support strong clarity.")
        elif clarity >= 70:
            explanation.append("Answer is clear but can be more detailed.")
        else:
            explanation.append("Answer is brief and may lack clarity.")

        if answer_data.get("off_topic", False):
            explanation.append("The answer appears off-topic, reducing relevance.")
        elif relevance >= 85:
            explanation.append("Answer is on-topic and relevant to the question.")
        else:
            explanation.append("Answer relevance is moderate and could be improved.")

        if completeness >= 100:
            explanation.append("The response includes strong detail and completeness.")
        else:
            explanation.append("The response is missing detail and lacks completeness.")

        if consistency >= 100:
            explanation.append("The response is consistent and specific.")
        else:
            explanation.append("The response is vague, which reduces consistency.")

        return {
            "question_id": question_id,
            "candidate_id": candidate_id,
            "answer_text": answer,
            "clarity": clarity,
            "relevance": relevance,
            "completeness": completeness,
            "consistency": consistency,
            "component_scores": {
                "clarity": clarity,
                "relevance": relevance,
                "completeness": completeness,
                "consistency": consistency
            },
            "final_score": final_score,
            "score_explanation": explanation
        }