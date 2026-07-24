import json
from pathlib import Path

from integrity_detection.integrity_framework import (
    IntegrityFramework
)


class IntegrityDesigner:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "integrity_design.json"
    )

    @staticmethod
    def generate():

        design = IntegrityFramework.describe()

        IntegrityDesigner.OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            IntegrityDesigner.OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                design,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            json.dumps(
                design,
                indent=4,
                ensure_ascii=False
            )
        )

        print(
            f"\nIntegrity design saved to:\n"
            f"{IntegrityDesigner.OUTPUT_FILE}"
        )

        return design


if __name__ == "__main__":

    IntegrityDesigner.generate()