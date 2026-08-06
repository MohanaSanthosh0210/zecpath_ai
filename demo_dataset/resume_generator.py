import json
import random
from pathlib import Path


class ResumeGenerator:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_DIR = (
        BASE_DIR /
        "config"
    )

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "resumes"
    )

    @staticmethod
    def generate():

        ResumeGenerator.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(

            ResumeGenerator.CONFIG_DIR /
            "candidate_levels.json",

            "r",

            encoding="utf-8"

        ) as file:

            levels = json.load(file)

        skills = [

            "Python",
            "Java",
            "SQL",
            "Docker",
            "FastAPI",
            "TensorFlow",
            "Power BI",
            "React"

        ]

        candidates = list(levels.keys())

        for index in range(10):

            level = random.choice(candidates)

            resume = {

                "candidate_id":

                    f"C{index+1:03}",

                "candidate_level":

                    level,

                "experience_years":

                    random.randint(0, 8),

                "skills":

                    random.sample(
                        skills,
                        4
                    ),

                "education":

                    "B.Tech Information Technology"

            }

            with open(

                ResumeGenerator.OUTPUT_DIR /
                f"candidate_{index+1:03}.json",

                "w",

                encoding="utf-8"

            ) as output:

                json.dump(

                    resume,

                    output,

                    indent=4,

                    ensure_ascii=False

                )


if __name__ == "__main__":

    ResumeGenerator.generate()

    print(
        "Demo resumes generated."
    )