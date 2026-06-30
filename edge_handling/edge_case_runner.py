import json
import os

from edge_handling.edge_case_handler import EdgeCaseHandler


class EdgeCaseRunner:

    INPUT_FILE = (
        "data/understood_answers/sample_answer.json"
    )

    def load_transcript(self):

        with open(
            self.INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data["structured_answer"]["text"]

    def run(self):

        transcript = self.load_transcript()

        handler = EdgeCaseHandler()

        report = handler.analyze(
            transcript
        )

        print(
            "\n========== EDGE CASE REPORT ==========\n"
        )

        print(
            json.dumps(
                report,
                indent=4
            )
        )

        print(
            "\nReport saved to "
            "data/edge_cases/edge_case_report.json"
        )


if __name__ == "__main__":

    EdgeCaseRunner().run()