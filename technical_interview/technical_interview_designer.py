import json
from pathlib import Path


class TechnicalInterviewDesigner:

    BASE_DIR = Path(__file__).resolve().parent

    CONFIG_DIR = BASE_DIR / "config"

    DATA_DIR = BASE_DIR / "data"

    OUTPUT_FILE = DATA_DIR / "technical_interview_design.json"

    CONFIG_FILES = [

        "interview_structure.json",

        "experience_levels.json",

        "role_skill_mapping.json",

        "difficulty_progression.json"

    ]

    @staticmethod
    def load_json(filename):

        filepath = (
            TechnicalInterviewDesigner.CONFIG_DIR /
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def build_design():

        design = {

            "system_name": "Technical Interview AI",

            "version": "1.0"

        }

        for file in TechnicalInterviewDesigner.CONFIG_FILES:

            key = file.replace(".json", "")

            design[key] = (

                TechnicalInterviewDesigner.load_json(file)

            )

        return design

    @staticmethod
    def save_design(design):

        TechnicalInterviewDesigner.DATA_DIR.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            TechnicalInterviewDesigner.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                design,

                file,

                indent=4,

                ensure_ascii=False

            )

    @staticmethod
    def generate():

        design = (

            TechnicalInterviewDesigner.build_design()

        )

        TechnicalInterviewDesigner.save_design(

            design

        )

        print(

            json.dumps(

                design,

                indent=4,

                ensure_ascii=False

            )

        )

        print(

            "\nTechnical Interview Design saved to:\n"

            f"{TechnicalInterviewDesigner.OUTPUT_FILE}"

        )

        return design


if __name__ == "__main__":

    TechnicalInterviewDesigner.generate()