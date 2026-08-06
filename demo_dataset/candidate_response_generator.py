import json
from pathlib import Path


class CandidateResponseGenerator:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "interview_responses"
    )

    @staticmethod
    def generate():

        CandidateResponseGenerator.OUTPUT_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        answers = [

            "I enjoy solving complex problems.",

            "Python is my primary programming language.",

            "I have worked on REST APIs.",

            "I prefer collaborative environments.",

            "Machine learning is one of my interests."

        ]

        for index in range(10):

            interview = {

                "candidate_id":

                    f"C{index+1:03}",

                "responses":

                    answers

            }

            with open(

                CandidateResponseGenerator.OUTPUT_DIR /
                f"response_{index+1:03}.json",

                "w",

                encoding="utf-8"

            ) as output:

                json.dump(

                    interview,

                    output,

                    indent=4,

                    ensure_ascii=False

                )


if __name__ == "__main__":

    CandidateResponseGenerator.generate()

    print(
        "Interview responses generated."
    )