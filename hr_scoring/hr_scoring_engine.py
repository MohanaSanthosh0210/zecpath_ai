import json
import os

from hr_scoring.weight_config import WeightConfig
from hr_scoring.relevance_scorer import RelevanceScorer
from hr_scoring.consistency_scorer import ConsistencyScorer
from hr_scoring.hr_score_calculator import HRScoreCalculator
from hr_scoring.score_normalizer import ScoreNormalizer


class HRInterviewScoringEngine:

    def __init__(self):

        self.answer_file = (
            "data/understood_answers/sample_answer.json"
        )

        self.communication_file = (
            "data/communication/communication_score.json"
        )

        self.behavior_file = (
            "data/behavioral_analysis/behavioral_report.json"
        )

    # ---------------------------------------------

    @staticmethod
    def load_json(path):

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

    # ---------------------------------------------

    def process(self):

        answer_data = self.load_json(
            self.answer_file
        )

        communication_data = self.load_json(
            self.communication_file
        )

        behavior_data = self.load_json(
            self.behavior_file
        )

        weights = WeightConfig.load_weights()

        relevance = RelevanceScorer.calculate(
            answer_data
        )

        consistency = ConsistencyScorer.calculate(
            answer_data
        )

        communication_score = (
            communication_data.get(
                "communication_score",
                0
            )
        )

        confidence_score = (
            behavior_data.get(
                "behavioral_confidence_score",
                0
            )
        )

        weighted_score = HRScoreCalculator.calculate(

            relevance["relevance_score"],

            communication_score,

            confidence_score,

            consistency["consistency_score"],

            weights

        )

        question_count = 1

        normalized_score = (

            ScoreNormalizer.normalize(

                weighted_score,

                question_count

            )

        )

        result = {

            "candidate_id":

                answer_data.get(

                    "candidate_id",

                    "UNKNOWN"

                ),

            "interview_questions":

                question_count,

            "score_breakdown": {

                "answer_relevance":

                    relevance["relevance_score"],

                "communication_score":

                    communication_score,

                "confidence_score":

                    confidence_score,

                "consistency_score":

                    consistency["consistency_score"]

            },

            "weights":

                weights,

            "weighted_score":

                weighted_score,

            "normalized_score":

                normalized_score

        }

        return result


if __name__ == "__main__":

    engine = HRInterviewScoringEngine()

    report = engine.process()

    print(

        "\n========== HR INTERVIEW ENGINE ==========\n"

    )

    print(

        json.dumps(

            report,

            indent=4

        )

    )