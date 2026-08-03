import json
from pathlib import Path

from stabilization.pipeline_validator import PipelineValidator
from stabilization.scoring_validator import ScoringValidator
from stabilization.conversation_validator import ConversationValidator
from stabilization.api_stabilizer import APIStabilizer
from stabilization.edge_case_tester import EdgeCaseTester


class StabilizationEngine:

    BASE_DIR = Path(__file__).resolve().parent

    REPORT_DIR = (
        BASE_DIR /
        "data" /
        "reports"
    )

    @staticmethod
    def run():

        StabilizationEngine.REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        pipeline = {

            "ats": {},
            "screening": {},
            "hr": {},
            "technical": {},
            "behavior": {},
            "integrity": {},
            "machine_test": {},
            "recommendation": {}

        }

        scores = {

            "ats": 86,
            "screening": 82,
            "hr": 88,
            "technical": 91,
            "behavior": 84,
            "integrity": 93,
            "machine_test": 87

        }

        conversation = [

            {

                "speaker": "AI",

                "text": "Introduce yourself."

            },

            {

                "speaker": "Candidate",

                "text": "I am a software engineer."

            }

        ]

        api_response = {

            "status": "success",

            "score": 87,

            "recommendation": "Hire"

        }

        results = {

            "pipeline_validation":

                PipelineValidator.validate(
                    pipeline
                ),

            "score_validation":

                ScoringValidator.validate_scores(
                    scores
                ),

            "conversation_validation":

                ConversationValidator.validate(
                    conversation
                ),

            "api_validation":

                APIStabilizer.validate(
                    api_response
                ),

            "edge_cases":

                EdgeCaseTester.run()

        }

        summary = {

            "system_status": "Stable",

            "pipeline_valid":

                results["pipeline_validation"]["valid"],

            "conversation_valid":

                results["conversation_validation"]["valid"],

            "api_valid":

                results["api_validation"]["valid"],

            "edge_cases_tested":

                len(results["edge_cases"])

        }

        with open(

            StabilizationEngine.REPORT_DIR /
            "stabilization_summary.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4,

                ensure_ascii=False

            )

        with open(

            StabilizationEngine.REPORT_DIR /
            "stability_report.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                results,

                file,

                indent=4,

                ensure_ascii=False

            )

        return summary


if __name__ == "__main__":

    print(

        json.dumps(

            StabilizationEngine.run(),

            indent=4

        )

    )