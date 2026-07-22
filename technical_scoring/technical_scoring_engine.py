from technical_scoring.accuracy_scorer import AccuracyScorer
from technical_scoring.depth_scorer import DepthScorer
from technical_scoring.reasoning_scorer import ReasoningScorer
from technical_scoring.applicability_scorer import ApplicabilityScorer
from technical_scoring.difficulty_normalizer import DifficultyNormalizer
from technical_scoring.rubric_loader import RubricLoader


class TechnicalScoringEngine:

    @staticmethod
    def evaluate(answer_data):

        weights = RubricLoader.load_weights()

        accuracy = AccuracyScorer.score(
            answer_data
        )["accuracy"]

        depth = DepthScorer.score(
            answer_data
        )["depth"]

        reasoning = ReasoningScorer.score(
            answer_data
        )["reasoning"]

        applicability = ApplicabilityScorer.score(
            answer_data
        )["applicability"]

        weighted_score = (

            accuracy * weights["accuracy"]

            +

            depth * weights["depth"]

            +

            reasoning * weights["reasoning"]

            +

            applicability * weights["applicability"]

        )

        difficulty = answer_data.get(
            "difficulty",
            "easy"
        )

        normalized = (

            DifficultyNormalizer.normalize(

                weighted_score,

                difficulty

            )

        )

        return {

            "skill_breakdown": {

                "accuracy": accuracy,

                "depth": depth,

                "reasoning": reasoning,

                "applicability": applicability

            },

            "weighted_score": round(

                weighted_score,

                2

            ),

            "normalized_score": normalized

        }


if __name__ == "__main__":

    sample = {

        "accuracy_score": 90,

        "depth_score": 85,

        "reasoning_score": 88,

        "applicability_score": 80,

        "difficulty": "hard"

    }

    print(

        TechnicalScoringEngine.evaluate(

            sample

        )

    )