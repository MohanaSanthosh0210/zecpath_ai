import json
import os


class AIScreeningPipeline:

    def __init__(self):

        self.paths = {

            "understood_answer":

                "data/understood_answers/sample_answer.json",

            "screening_score":

                "data/screening_scores/final_scores/unknown.json",

            "behavior_report":

                "data/behavioral_reports/sample_answer.json",

            "screening_report":

                "data/screening_reports/sample_answer.json",

            "conversation":

                "data/conversation_flow/conversation_decision.json",

            "edge_case":

                "data/edge_cases/edge_case_report.json"

        }

    # ----------------------------------

    # Generic JSON Loader

    # ----------------------------------

    def load_json(self, path):

        if not os.path.exists(path):

            return None

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    # ----------------------------------

    # Load Complete Pipeline

    # ----------------------------------

    def run(self):

        result = {}

        for key, path in self.paths.items():

            result[key] = self.load_json(path)

        return result