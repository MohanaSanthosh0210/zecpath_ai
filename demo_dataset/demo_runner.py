import json
from pathlib import Path

from demo_dataset.resume_generator import (
    ResumeGenerator
)

from demo_dataset.job_generator import (
    JobGenerator
)

from demo_dataset.candidate_response_generator import (
    CandidateResponseGenerator
)

from demo_dataset.pipeline_simulator import (
    PipelineSimulator
)

from demo_dataset.dataset_validator import (
    DatasetValidator
)


class DemoRunner:

    BASE_DIR = Path(__file__).resolve().parent

    OUTPUT_FILE = (
        BASE_DIR /
        "data" /
        "simulation_summary.json"
    )

    @staticmethod
    def run():

        print(
            "\nGenerating demo resumes..."
        )

        ResumeGenerator.generate()

        print(
            "Generating job descriptions..."
        )

        JobGenerator.generate()

        print(
            "Generating interview responses..."
        )

        CandidateResponseGenerator.generate()

        print(
            "Validating dataset..."
        )

        validation = (
            DatasetValidator.validate()
        )

        if not validation["valid"]:

            print(
                "Dataset validation failed."
            )

            print(
                validation
            )

            return

        print(
            "Running end-to-end simulation..."
        )

        reports = (
            PipelineSimulator.simulate()
        )

        selected = sum(

            1

            for report in reports

            if report["decision"] == "Selected"

        )

        rejected = len(reports) - selected

        average_score = round(

            sum(

                report["overall_score"]

                for report in reports

            ) / len(reports),

            2

        )

        summary = {

            "total_candidates":

                len(reports),

            "selected":

                selected,

            "rejected":

                rejected,

            "average_score":

                average_score,

            "simulation_status":

                "Completed"

        }

        DemoRunner.OUTPUT_FILE.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            DemoRunner.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                summary,

                file,

                indent=4,

                ensure_ascii=False

            )

        print()

        print(
            "Demo dataset generated successfully."
        )

        print(
            f"Simulation completed for {len(reports)} candidates."
        )

        print(
            f"Selected : {selected}"
        )

        print(
            f"Rejected : {rejected}"
        )


if __name__ == "__main__":

    DemoRunner.run()