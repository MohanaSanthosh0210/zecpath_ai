import os
import json


class PipelineValidator:

    REQUIRED_FILES = {

        "understood_answer":
            "data/understood_answers/sample_answer.json",

        "screening_score":
            "data/screening_scores/final_scores/unknown.json",

        "behavior_report":
            "data/behavioral_reports/sample_answer.json",

        "screening_report":
            "data/screening_reports/sample_answer.json",

        "conversation":
            "data/conversation_flow/conversation_decision.json"

    }

    @classmethod
    def validate(cls):

        results = {}

        for name, path in cls.REQUIRED_FILES.items():

            exists = os.path.exists(path)

            results[name] = exists

        return results

    @classmethod
    def load_json(cls, path):

        with open(path, "r", encoding="utf-8") as file:

            return json.load(file)
        