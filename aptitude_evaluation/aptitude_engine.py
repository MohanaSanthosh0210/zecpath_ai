import json
import os

from aptitude_evaluation.reasoning_question_engine import (
    ReasoningQuestionEngine
)

from aptitude_evaluation.logical_reasoning_scorer import (
    LogicalReasoningScorer
)

from aptitude_evaluation.scenario_evaluator import (
    ScenarioEvaluator
)

from aptitude_evaluation.problem_solving_analyzer import (
    ProblemSolvingAnalyzer
)

from aptitude_evaluation.answer_pattern_mapper import (
    AnswerPatternMapper
)


class AptitudeEngine:

    ANSWER_FILE = (
        "data/understood_answers/sample_answer.json"
    )

    ANSWER_DIR = (
        "data/understood_answers"
    )

    OUTPUT_FOLDER = (
        "data/aptitude"
    )

    OUTPUT_FILE = (
        "data/aptitude/aptitude_report.json"
    )

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

    @classmethod
    def resolve_answer_source(cls):

        if os.path.isdir(cls.ANSWER_DIR):

            json_files = [
                os.path.join(cls.ANSWER_DIR, name)
                for name in os.listdir(cls.ANSWER_DIR)
                if name.endswith(".json")
            ]

            if json_files:

                latest_file = max(
                    json_files,
                    key=os.path.getmtime
                )

                return latest_file

        return cls.ANSWER_FILE

    @staticmethod
    def extract_candidate_answer(answer_data):

        structured_answer = answer_data.get(
            "structured_answer",
            {}
        )

        if isinstance(structured_answer, dict):

            text = structured_answer.get("text")

            if text:

                return text

        interview_answers = answer_data.get("interview_answers")

        if isinstance(interview_answers, list):
            for item in interview_answers:
                if isinstance(item, dict):
                    answer_text = item.get("answer_text") or item.get("answer") or item.get("text")
                    if isinstance(answer_text, str) and answer_text.strip():
                        return answer_text

        for key in [
            "answer_text",
            "text",
            "response",
            "answer"
        ]:

            value = answer_data.get(key)

            if isinstance(value, str) and value.strip():

                return value

        return ""

    def process(self):

        answer_path = self.resolve_answer_source()

        answer_data = self.load_json(
            answer_path
        )

        candidate_answer = self.extract_candidate_answer(
            answer_data
        )

        scenario = (

            ReasoningQuestionEngine

            .get_random_question()

        )

        reasoning = (

            LogicalReasoningScorer

            .calculate(

                candidate_answer,

                scenario[
                    "expected_keywords"
                ]

            )

        )

        scenario_result = (

            ScenarioEvaluator

            .evaluate(

                candidate_answer,

                scenario[
                    "expected_keywords"
                ]

            )

        )

        problem_solving = (

            ProblemSolvingAnalyzer

            .analyze(

                candidate_answer

            )

        )

        pattern = (

            AnswerPatternMapper

            .map(

                candidate_answer

            )

        )

        final_score = round(

            (

                reasoning[
                    "logical_reasoning_score"
                ]

                +

                scenario_result[
                    "scenario_score"
                ]

                +

                problem_solving[
                    "problem_solving_score"
                ]

                +

                pattern[
                    "answer_pattern_score"
                ]

            )

            / 4,

            2

        )

        bank = ReasoningQuestionEngine.load_question_bank()

        report = {

            "candidate_id":

                answer_data.get(

                    "candidate_id",

                    "UNKNOWN"

                ),

            "answer_source": {
                "source_file": answer_path,
                "source_type": "latest_understood_answer"
            },

            "candidate_answer": candidate_answer,

            "aptitude_design": {
                "objective": "Assess reasoning, situational judgment, and problem-solving clarity",
                "scoring_components": [
                    "logical_reasoning",
                    "scenario_evaluation",
                    "problem_solving",
                    "answer_pattern"
                ],
                "scenario_count": len(bank),
                "question_bank_source": self.QUESTION_BANK if hasattr(self, "QUESTION_BANK") else ReasoningQuestionEngine.QUESTION_BANK
            },

            "scenario":

                scenario,

            "logical_reasoning":

                reasoning,

            "scenario_evaluation":

                scenario_result,

            "problem_solving":

                problem_solving,

            "answer_pattern":

                pattern,

            "aptitude_score":

                final_score

        }

        os.makedirs(

            self.OUTPUT_FOLDER,

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

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

    engine = AptitudeEngine()

    report = engine.process()

    print(

        json.dumps(

            report,

            indent=4

        )

    )