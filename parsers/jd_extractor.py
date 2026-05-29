import os
import json

from jd_parser import extract_job_data
from jd_cleaner import clean_jd_text

INPUT_FOLDER = "data/job_descriptions"
OUTPUT_FOLDER = "data/structured_jobs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    file_path = os.path.join(INPUT_FOLDER, file)

    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_text = clean_jd_text(raw_text)

    structured_data = extract_job_data(cleaned_text)

    output_file = os.path.join(
        OUTPUT_FOLDER,
        file.split(".")[0] + ".json"
    )

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(structured_data, out, indent=4)

    print(f"Processed JD: {file}")