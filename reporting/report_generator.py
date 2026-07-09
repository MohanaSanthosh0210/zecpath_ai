import os

from reporting.report_utils import (
    load_json,
    save_json
)

from reporting.screening_report_builder import (
    ScreeningReportBuilder
)
from reporting.interview_summary_generator import (
    InterviewSummaryGenerator
)


UNDERSTOOD_ANSWERS_DIR = (
    "data/understood_answers"
)

BEHAVIORAL_REPORTS_DIR = (
    "data/behavioral_reports"
)

FINAL_SCORES_DIR = (
    "data/screening_scores/final_scores"
)

OUTPUT_DIR = (
    "data/screening_reports"
)


def get_matching_behavior_file(answer_file):

    base_name = os.path.basename(answer_file)

    behavior_file = os.path.join(
        BEHAVIORAL_REPORTS_DIR,
        base_name
    )

    if os.path.exists(behavior_file):
        return behavior_file

    return None


def get_matching_score_file():

    score_files = [
        f for f in os.listdir(FINAL_SCORES_DIR)
        if f.endswith(".json")
    ]

    if not score_files:
        return None

    return os.path.join(
        FINAL_SCORES_DIR,
        score_files[0]
    )


def generate_interview_summary_reports():

    os.makedirs(
        "data/interview_summaries",
        exist_ok=True
    )

    generator = InterviewSummaryGenerator(
        output_dir="data/interview_summaries"
    )

    answer_data = load_json(
        os.path.join(
            UNDERSTOOD_ANSWERS_DIR,
            "sample_answer.json"
        )
    )
    communication_data = load_json(
        "data/communication/communication_score.json"
    )
    behavior_data = load_json(
        "data/behavioral_analysis/behavioral_report.json"
    )
    hr_score_data = load_json(
        "data/hr_scoring/hr_score_report.json"
    )

    report = generator.generate_and_save(
        answer_data=answer_data,
        communication_data=communication_data,
        behavior_data=behavior_data,
        hr_score_data=hr_score_data,
        output_file="data/interview_summaries/sample_hr_summary.json",
    )

    print(
        "Generated interview summary -> data/interview_summaries/sample_hr_summary.json"
    )

    return report


def generate_screening_reports():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    score_file = get_matching_score_file()

    if score_file is None:

        print(
            "No final screening score found."
        )

        return

    screening_score = load_json(
        score_file
    )

    answer_files = [

        f

        for f in os.listdir(
            UNDERSTOOD_ANSWERS_DIR
        )

        if f.endswith(".json")
    ]

    if not answer_files:

        print(
            "No understood answers found."
        )

        return

    generated = 0

    for file_name in answer_files:

        answer_path = os.path.join(
            UNDERSTOOD_ANSWERS_DIR,
            file_name
        )

        behavior_path = get_matching_behavior_file(
            answer_path
        )

        if behavior_path is None:

            print(
                f"Behavior report missing for {file_name}"
            )

            continue

        understanding = load_json(
            answer_path
        )

        behavior = load_json(
            behavior_path
        )

        builder = ScreeningReportBuilder(

            understanding,

            screening_score,

            behavior

        )

        report = builder.build_report()

        output_file = os.path.join(

            OUTPUT_DIR,

            file_name

        )

        save_json(
            report,
            output_file
        )

        generated += 1

        print(
            f"Generated report -> {output_file}"
        )

    print()

    print(
        f"Successfully generated {generated} recruiter report(s)."
    )


if __name__ == "__main__":

    generate_screening_reports()
    generate_interview_summary_reports()