import json
from pathlib import Path

from machine_test_ai.evaluation_framework import (
    EvaluationFramework
)


class MachineTestDesigner:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "machine_test_design.json"
    )

    @staticmethod
    def generate():

        design = EvaluationFramework.describe()

        MachineTestDesigner.OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            MachineTestDesigner.OUTPUT_FILE,
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
            f"\nMachine Test AI design saved to:\n"
            f"{MachineTestDesigner.OUTPUT_FILE}"
        )

        return design


if __name__ == "__main__":

    MachineTestDesigner.generate()