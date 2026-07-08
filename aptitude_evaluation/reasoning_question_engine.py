import json
import os
import random


class ReasoningQuestionEngine:

    QUESTION_BANK = (
        "aptitude_evaluation/config/scenario_bank.json"
    )

    @staticmethod
    def resolve_question_bank_path():

        candidate_paths = [
            ReasoningQuestionEngine.QUESTION_BANK,
            os.path.join(
                os.path.dirname(__file__),
                "config",
                "scenario_bank.json"
            ),
            os.path.join(
                os.getcwd(),
                "aptitude_evaluation",
                "config",
                "scenario_bank.json"
            )
        ]

        for path in candidate_paths:
            if os.path.exists(path):
                return path

        raise FileNotFoundError("Scenario bank not found.")

    @staticmethod
    def load_question_bank():

        path = ReasoningQuestionEngine.resolve_question_bank_path()

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def get_random_question():

        bank = (

            ReasoningQuestionEngine.load_question_bank()

        )

        return random.choice(bank)

    @staticmethod
    def get_question_by_category(category):

        bank = (

            ReasoningQuestionEngine.load_question_bank()

        )

        questions = [

            q

            for q in bank

            if q["category"] == category

        ]

        if not questions:

            return None

        return random.choice(questions)


if __name__ == "__main__":

    print(

        ReasoningQuestionEngine.get_random_question()

    )