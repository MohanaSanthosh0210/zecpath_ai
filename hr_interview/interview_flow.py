import json
import os

from hr_interview.question_bank import QuestionBank


class InterviewFlow:

    OUTPUT_FILE = (
        "data/hr_interview/interview_design.json"
    )

    def __init__(self):

        self.question_bank = QuestionBank()

    def build(

        self,

        experience_level,

        role_type

    ):

        questions = self.question_bank.build_question_bank(

            experience_level,

            role_type

        )

        flow = {

            "experience_level":

                experience_level,

            "role_type":

                role_type,

            "phases": [

                {

                    "phase":

                        "INTRODUCTION",

                    "questions":

                        questions[0:1]

                },

                {

                    "phase":

                        "CORE_HR",

                    "questions":

                        questions[1:8]

                },

                {

                    "phase":

                        "ROLE_BASED",

                    "questions":

                        questions[8:]

                },

                {

                    "phase":

                        "CLOSING",

                    "questions": [

                        {

                            "id":

                                "CLOSE_001",

                            "question":

                                "Do you have any questions for us?"

                        }

                    ]

                }

            ]

        }

        return flow

    def save(

        self,

        experience_level,

        role_type

    ):

        flow = self.build(

            experience_level,

            role_type

        )

        os.makedirs(

            "data/hr_interview",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                flow,

                file,

                indent=4

            )

        print(

            "\nInterview flow saved successfully."

        )

        print(

            json.dumps(

                flow,

                indent=4

            )

        )

        return flow