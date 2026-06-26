import os

from reporting.report_utils import (
    load_json,
    save_json
)

from reporting.screening_report_builder import (
    ScreeningReportBuilder
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