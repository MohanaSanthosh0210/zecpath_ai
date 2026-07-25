import json
from pathlib import Path


class MachineTestReportGenerator:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "machine_test_reports"
    )

    @staticmethod
    def generate(result):

        report = {

            "candidate_id": result.get(
                "candidate_id",
                "UNKNOWN"
            ),

            "task_type": result.get(
                "task_type",
                "UNKNOWN"
            ),

            "difficulty": result.get(
                "difficulty",
                "UNKNOWN"
            ),

            "correctness": result.get(
                "correctness",
                0
            ),

            "efficiency": result.get(
                "efficiency",
                0
            ),

            "code_quality": result.get(
                "code_quality",
                0
            ),

            "problem_solving": result.get(
                "problem_solving",
                0
            ),

            "final_score": result.get(
                "final_score",
                0
            )

        }

        MachineTestReportGenerator.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        filepath = (
            MachineTestReportGenerator.OUTPUT_DIR /
            "machine_test_report.json"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False
            )
        )

        print(
            f"\nReport saved to:\n{filepath}"
        )

        return report


if __name__ == "__main__":

    sample = {

        "candidate_id": "C101",

        "task_type": "coding_problem",

        "difficulty": "medium",

        "correctness": 90,

        "efficiency": 82,

        "code_quality": 88,

        "problem_solving": 91,

        "final_score": 88.5

    }

    MachineTestReportGenerator.generate(sample)