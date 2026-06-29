import os
import json

from testing.metrics import Metrics
from testing.pipeline_validator import PipelineValidator


class ScreeningSystemTester:

    def __init__(self):

        self.validation = PipelineValidator.validate()

    def run(self):

        print("\n========== PIPELINE VALIDATION ==========\n")

        for module, status in self.validation.items():

            print(f"{module:<20} : {'OK' if status else 'MISSING'}")

        if not all(self.validation.values()):

            print("\nPipeline incomplete.")

            return

        understood = PipelineValidator.load_json(

            "data/understood_answers/sample_answer.json"

        )

        screening = PipelineValidator.load_json(

            "data/screening_scores/final_scores/unknown.json"

        )

        behavior = PipelineValidator.load_json(

            "data/behavioral_reports/sample_answer.json"

        )

        report = PipelineValidator.load_json(

            "data/screening_reports/sample_answer.json"

        )

        conversation = PipelineValidator.load_json(

            "data/conversation_flow/conversation_decision.json"

        )

        screening_score = screening.get(
            "final_screening_score",
            0
        )

        confidence = behavior.get(
            "confidence",
            {}
        ).get(
            "confidence_score",
            0
        )

        sentiment = behavior.get(
            "sentiment",
            {}
        ).get(
            "sentiment",
            "Unknown"
        )

        communication = behavior.get(
            "communication_strength",
            "Unknown"
        )

        intent = understood.get(
            "intent",
            "unknown"
        )

        state = conversation.get(
            "state",
            "UNKNOWN"
        )

        summary = {

            "tested_candidates": 1,

            "average_screening_score":
                Metrics.average(
                    [screening_score]
                ),

            "average_confidence":
                Metrics.average(
                    [confidence]
                ),

            "communication_strength":
                communication,

            "sentiment_distribution":
                Metrics.distribution(
                    [sentiment]
                ),

            "intent_distribution":
                Metrics.distribution(
                    [intent]
                ),

            "conversation_state":
                state,

            "pipeline_status":
                "PASS"

        }

        os.makedirs(

            "data/test_results",

            exist_ok=True

        )

        with open(

            "data/test_results/screening_test_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4

            )

        print("\n========== SCREENING TEST REPORT ==========\n")

        print(

            json.dumps(

                summary,

                indent=4

            )

        )

        print(

            "\nReport saved to "

            "data/test_results/screening_test_report.json"

        )


if __name__ == "__main__":

    tester = ScreeningSystemTester()

    tester.run()