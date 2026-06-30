import os
import json


class DocumentationGenerator:

    EDGE_CASE_FILE = (
        "data/edge_cases/edge_case_report.json"
    )

    OUTPUT_FILE = (
        "data/documentation/edge_case_documentation.json"
    )

    def generate(self):

        with open(
            self.EDGE_CASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)

        detection = report["edge_case_detection"]

        action = report["system_action"]

        documentation = {

            "summary": {

                "audio_quality":

                    detection["audio_quality"]["audio_quality"],

                "language_mix":

                    detection["language_mix"]["language_mix"],

                "missing_answer":

                    detection["missing_answer"],

                "background_noise":

                    detection["background_noise"]["background_noise"]

            },

            "system_action": action,

            "recommendation": self.get_recommendation(

                detection,

                action

            )

        }

        os.makedirs(

            "data/documentation",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                documentation,

                file,

                indent=4

            )

        return documentation

    def get_recommendation(

        self,

        detection,

        action

    ):

        recommendations = []

        if detection["audio_quality"]["audio_quality"] == "Poor":

            recommendations.append(

                "Use a better microphone or improve network quality."

            )

        if detection["language_mix"]["language_mix"]:

            recommendations.append(

                "Ask the candidate to answer using a single language."

            )

        if detection["missing_answer"]:

            recommendations.append(

                "Prompt the candidate to provide a complete answer."

            )

        if detection["background_noise"]["background_noise"]:

            recommendations.append(

                "Move to a quieter environment before continuing."

            )

        if action["status"] == "Fallback":

            recommendations.append(

                "Escalate the interview to a human recruiter."

            )

        if not recommendations:

            recommendations.append(

                "No issues detected. Continue the interview."

            )

        return recommendations