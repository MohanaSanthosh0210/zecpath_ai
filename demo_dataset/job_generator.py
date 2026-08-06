import json
from pathlib import Path


class JobGenerator:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_DIR = (
        BASE_DIR /
        "config"
    )

    OUTPUT_DIR = (
        BASE_DIR /
        "data" /
        "job_descriptions"
    )

    @staticmethod
    def generate():

        JobGenerator.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(

            JobGenerator.CONFIG_DIR /
            "job_roles.json",

            "r",

            encoding="utf-8"

        ) as file:

            jobs = json.load(file)

        for index, role in enumerate(

            jobs["roles"][:5]

        ):

            job = {

                "job_id":

                    f"J{index+1:03}",

                "role":

                    role,

                "required_skills": [

                    "Python",

                    "SQL",

                    "Problem Solving"

                ],

                "experience_required":

                    "2+ Years"

            }

            with open(

                JobGenerator.OUTPUT_DIR /
                f"job_{index+1:03}.json",

                "w",

                encoding="utf-8"

            ) as output:

                json.dump(

                    job,

                    output,

                    indent=4,

                    ensure_ascii=False

                )


if __name__ == "__main__":

    JobGenerator.generate()

    print(
        "Demo job descriptions generated."
    )