import json
import os

from behavioral_intelligence.confidence_analyzer import (
    ConfidenceAnalyzer
)

from behavioral_intelligence.sentiment_engine import (
    SentimentEngine
)

from behavioral_intelligence.contradiction_detector import (
    ContradictionDetector
)

from behavioral_intelligence.stress_indicator import (
    StressIndicator
)


class BehavioralConfidenceEngine:

    def __init__(self):

        self.answer_file = (
            "data/understood_answers/sample_answer.json"
        )

        self.communication_file = (
            "data/communication/communication_score.json"
        )

        self.output_file = (
            "data/behavioral_analysis/behavioral_report.json"
        )

    # ------------------------------------------

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

    # ------------------------------------------

    def behavioral_score(

        self,

        confidence,

        sentiment,

        contradiction,

        stress,

        communication

    ):

        confidence_score = confidence[
            "confidence_score"
        ]

        sentiment_score = sentiment[
            "sentiment_score"
        ]

        contradiction_score = contradiction[
            "contradiction_score"
        ]

        stress_score = stress[
            "stress_score"
        ]

        communication_score = communication[
            "communication_score"
        ]

        final_score = (

            confidence_score * 0.40 +

            communication_score * 0.25 +

            sentiment_score * 0.15 +

            (100 - stress_score) * 0.10 +

            contradiction_score * 0.10

        )

        return round(

            final_score,

            2

        )

    # ------------------------------------------

    def process(self):

        answer_json = self.load_json(

            self.answer_file

        )

        communication_json = self.load_json(

            self.communication_file

        )

        answer = (

            answer_json

            .get(

                "structured_answer",

                {}

            )

            .get(

                "text",

                ""

            )

        )

        confidence = (

            ConfidenceAnalyzer.analyze(

                answer

            )

        )

        sentiment = (

            SentimentEngine.analyze(

                answer

            )

        )

        contradiction = (

            ContradictionDetector.detect(

                answer_json

            )

        )

        stress = (

            StressIndicator.analyze(

                confidence,

                sentiment

            )

        )

        behavioral_score = (

            self.behavioral_score(

                confidence,

                sentiment,

                contradiction,

                stress,

                communication_json

            )

        )

        report = {

            "candidate_id":

                answer_json.get(

                    "candidate_id",

                    "UNKNOWN"

                ),

            "intent":

                answer_json.get(

                    "intent"

                ),

            "confidence":

                confidence,

            "sentiment":

                sentiment,

            "contradictions":

                contradiction,

            "stress":

                stress,

            "communication_score":

                communication_json[

                    "communication_score"

                ],

            "behavioral_confidence_score":

                behavioral_score

        }

        os.makedirs(

            "data/behavioral_analysis",

            exist_ok=True

        )

        with open(

            self.output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4

            )

        return report


if __name__ == "__main__":

    engine = BehavioralConfidenceEngine()

    result = engine.process()

    print(

        "\n========== BEHAVIORAL REPORT ==========\n"

    )

    print(

        json.dumps(

            result,

            indent=4

        )

    )

    print(

        "\nBehavioral report saved to:\n"

        "data/behavioral_analysis/behavioral_report.json"

    )