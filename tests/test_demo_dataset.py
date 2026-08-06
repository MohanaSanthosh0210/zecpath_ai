from pathlib import Path
import json


class DemoDatasetTest:

    PROJECT_ROOT = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    BASE_DIR = (
        PROJECT_ROOT /
        "demo_dataset"
    )

    REQUIRED_FOLDERS = [

        "data/resumes",
        "data/job_descriptions",
        "data/interview_responses",
        "data/ats_results",
        "data/screening_results",
        "data/interview_results",
        "data/hiring_reports"

    ]

    REQUIRED_FILES = [

        "data/simulation_summary.json"

    ]

    @staticmethod
    def validate_folders():

        missing = []

        for folder in DemoDatasetTest.REQUIRED_FOLDERS:

            path = (
                DemoDatasetTest.BASE_DIR /
                folder
            )

            if (
                not path.exists()
                or
                len(list(path.glob("*"))) == 0
            ):

                missing.append(folder)

        return missing

    @staticmethod
    def validate_files():

        missing = []

        for file in DemoDatasetTest.REQUIRED_FILES:

            path = (
                DemoDatasetTest.BASE_DIR /
                file
            )

            if not path.exists():

                missing.append(file)

        return missing

    @staticmethod
    def validate_summary():

        summary_path = (

            DemoDatasetTest.BASE_DIR /
            "data" /
            "simulation_summary.json"

        )

        with open(

            summary_path,

            "r",

            encoding="utf-8"

        ) as file:

            summary = json.load(file)

        required_keys = [

            "total_candidates",

            "selected",

            "rejected",

            "average_score",

            "simulation_status"

        ]

        return all(

            key in summary

            for key in required_keys

        )


if __name__ == "__main__":

    folders = DemoDatasetTest.validate_folders()

    files = DemoDatasetTest.validate_files()

    summary_ok = (
        DemoDatasetTest.validate_summary()
    )

    if not folders:

        print("✓ Folder validation passed")

    else:

        print(
            "Missing folders:",
            folders
        )

    if not files:

        print("✓ File validation passed")

    else:

        print(
            "Missing files:",
            files
        )

    if summary_ok:

        print(
            "✓ Simulation summary validated"
        )

    else:

        print(
            "Simulation summary validation failed"
        )