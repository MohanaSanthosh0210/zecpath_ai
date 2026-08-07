import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "data" / "mock_demo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class QASimulator:

    @staticmethod
    def generate():

        qa = {

            "questions": [

                {

                    "question": "Why Zecpath AI?",

                    "answer": "To automate and improve the recruitment process using AI."

                },

                {

                    "question": "How is ATS score calculated?",

                    "answer": "By comparing candidate skills, education, projects and experience with job requirements."

                },

                {

                    "question": "What does Decision AI do?",

                    "answer": "It combines ATS, Screening, HR and Technical interview scores to recommend a hiring decision."

                }

            ]

        }

        with open(

            OUTPUT_DIR / "qa_session.json",

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(qa, file, indent=4)

        return qa