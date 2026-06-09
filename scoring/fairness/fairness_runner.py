import os
import json
import glob

from scoring.fairness.resume_normalizer import normalize_resume
from scoring.fairness.bias_detector import remove_bias_fields

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INPUT_DIR = os.path.join(
    ROOT_DIR,
    "data",
    "sectioned_resumes"
)

OUTPUT_DIR = os.path.join(
    ROOT_DIR,
    "data",
    "normalized_resumes"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_resume_file(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        resume = json.load(f)

    # Remove bias fields
    resume = remove_bias_fields(resume)

    # Normalize structure
    resume = normalize_resume(resume)

    output_file = os.path.join(
        OUTPUT_DIR,
        os.path.basename(file_path)
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            resume,
            f,
            indent=4
        )

    print(
        f"Processed: {os.path.basename(file_path)}"
    )


def main():

    resume_files = glob.glob(
        os.path.join(INPUT_DIR, "*.json")
    )

    if not resume_files:
        print(
            "No resumes found in data/sectioned_resumes"
        )
        return

    print(
        f"Found {len(resume_files)} resumes\n"
    )

    for resume_file in resume_files:
        process_resume_file(
            resume_file
        )

    print(
        "\nNormalization Complete"
    )
    print(
        f"Output Folder: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()