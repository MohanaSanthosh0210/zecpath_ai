import os
import json


class ScreeningEvaluationReport:

    OUTPUT_FILE = (
        "data/evaluation/screening_ai_evaluation.json"
    )

    def load_json(self, path):

        if not os.path.exists(path):
            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def generate(self):

        understood = self.load_json(
            "data/understood_answers/sample_answer.json"
        )

        screening = self.load_json(
            "data/screening_scores/final_scores/unknown.json"
        )

        behavior = self.load_json(
            "data/behavioral_reports/sample_answer.json"
        )

        report = self.load_json(
            "data/screening_reports/sample_answer.json"
        )

        conversation = self.load_json(
            "data/conversation_flow/conversation_decision.json"
        )

        edge = self.load_json(
            "data/edge_cases/edge_case_report.json"
        )

        evaluation = {

            "candidate_information": {

                "intent":
                    understood.get("intent"),

                "skills":
                    understood.get("skills"),

                "experience":
                    understood.get("experience")

            },

            "screening_result": {

                "screening_score":
                    screening.get(
                        "final_screening_score"
                    ),

                "status":
                    screening.get(
                        "status"
                    )

            },

            "behavior_analysis": {

                "communication_strength":

                    behavior.get(
                        "communication_strength"
                    ),

                "confidence":

                    behavior.get(
                        "confidence"
                    ),

                "sentiment":

                    behavior.get(
                        "sentiment"
                    )

            },

            "screening_report":

                report,

            "conversation_flow":

                conversation,

            "edge_case_analysis":

                edge,

            "overall_ai_recommendation":

                self.generate_recommendation(

                    screening,

                    behavior,

                    edge

                )

        }

        os.makedirs(

            "data/evaluation",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                evaluation,

                file,

                indent=4

            )

        print(
            "\n========== SCREENING AI EVALUATION ==========\n"
        )

        print(
            json.dumps(
                evaluation,
                indent=4
            )
        )

        print(
            "\nEvaluation report saved to "
            "data/evaluation/screening_ai_evaluation.json"
        )

    def generate_recommendation(

        self,

        screening,

        behavior,

        edge

    ):

        score = screening.get(

            "final_screening_score",

            0

        )

        communication = behavior.get(

            "communication_strength",

            "Weak"

        )

        edge_action = edge.get(

            "system_action",

            {}

        ).get(

            "status",

            "Continue"

        )

        if edge_action == "Fallback":

            return {

                "decision":

                    "Manual Recruiter Review",

                "reason":

                    "Critical edge cases detected."

            }

        if score >= 85:

            return {

                "decision":

                    "Strongly Recommended",

                "reason":

                    "Excellent overall performance."

            }

        if score >= 70:

            return {

                "decision":

                    "Recommended",

                "reason":

                    "Good screening performance."

            }

        if communication == "Strong":

            return {

                "decision":

                    "Review",

                "reason":

                    "Good communication but screening score requires recruiter review."

            }

        return {

            "decision":

                "Not Recommended",

            "reason":

                "Low screening performance."

        }


if __name__ == "__main__":

    ScreeningEvaluationReport().generate()