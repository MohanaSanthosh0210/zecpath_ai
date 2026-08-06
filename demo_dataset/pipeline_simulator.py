import json
import random
from pathlib import Path


class PipelineSimulator:

    BASE_DIR = Path(__file__).resolve().parent

    RESUME_DIR = (
        BASE_DIR /
        "data" /
        "resumes"
    )

    JOB_DIR = (
        BASE_DIR /
        "data" /
        "job_descriptions"
    )

    ATS_DIR = (
        BASE_DIR /
        "data" /
        "ats_results"
    )

    SCREENING_DIR = (
        BASE_DIR /
        "data" /
        "screening_results"
    )

    INTERVIEW_DIR = (
        BASE_DIR /
        "data" /
        "interview_results"
    )

    REPORT_DIR = (
        BASE_DIR /
        "data" /
        "hiring_reports"
    )

    @staticmethod
    def initialize():

        for directory in [

            PipelineSimulator.ATS_DIR,
            PipelineSimulator.SCREENING_DIR,
            PipelineSimulator.INTERVIEW_DIR,
            PipelineSimulator.REPORT_DIR

        ]:

            directory.mkdir(
                parents=True,
                exist_ok=True
            )

    @staticmethod
    def simulate():

        PipelineSimulator.initialize()

        resumes = sorted(

            PipelineSimulator.RESUME_DIR.glob(
                "*.json"
            )

        )

        jobs = sorted(

            PipelineSimulator.JOB_DIR.glob(
                "*.json"
            )

        )

        if not jobs:

            raise FileNotFoundError(
                "No demo job descriptions found."
            )

        job = json.loads(
            jobs[0].read_text(
                encoding="utf-8"
            )
        )

        summary = []

        for resume_file in resumes:

            resume = json.loads(

                resume_file.read_text(
                    encoding="utf-8"
                )

            )

            candidate = resume["candidate_id"]

            ats_score = random.randint(
                45,
                95
            )

            screening_score = random.randint(
                40,
                95
            )

            technical_score = random.randint(
                40,
                95
            )

            hr_score = random.randint(
                40,
                95
            )

            overall = round(

                (
                    ats_score +
                    screening_score +
                    technical_score +
                    hr_score

                ) / 4,

                2

            )

            decision = (
                "Selected"
                if overall >= 80
                else
                "Rejected"
            )

            ats = {

                "candidate_id": candidate,
                "job_id": job["job_id"],
                "ats_score": ats_score

            }

            screening = {

                "candidate_id": candidate,
                "screening_score": screening_score

            }

            interview = {

                "candidate_id": candidate,
                "technical_score": technical_score,
                "hr_score": hr_score

            }

            report = {

                "candidate_id": candidate,
                "overall_score": overall,
                "decision": decision

            }

            (
                PipelineSimulator.ATS_DIR /
                f"{candidate}.json"

            ).write_text(

                json.dumps(
                    ats,
                    indent=4
                ),

                encoding="utf-8"

            )

            (
                PipelineSimulator.SCREENING_DIR /
                f"{candidate}.json"

            ).write_text(

                json.dumps(
                    screening,
                    indent=4
                ),

                encoding="utf-8"

            )

            (
                PipelineSimulator.INTERVIEW_DIR /
                f"{candidate}.json"

            ).write_text(

                json.dumps(
                    interview,
                    indent=4
                ),

                encoding="utf-8"

            )

            (
                PipelineSimulator.REPORT_DIR /
                f"{candidate}.json"

            ).write_text(

                json.dumps(
                    report,
                    indent=4
                ),

                encoding="utf-8"

            )

            summary.append(report)

        return summary


if __name__ == "__main__":

    reports = PipelineSimulator.simulate()

    print(
        f"Simulation completed for {len(reports)} candidates."
    )