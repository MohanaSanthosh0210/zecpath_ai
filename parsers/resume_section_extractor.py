import json
import os

from section_classifier import detect_sections

INPUT_FOLDER = "data/cleaned"
OUTPUT_FOLDER = "data/sectioned_resumes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file_name in os.listdir(INPUT_FOLDER):

    if not file_name.endswith(".json"):
        continue

    input_path = os.path.join(INPUT_FOLDER, file_name)

    with open(
        input_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    text = data.get("cleaned_text", "")

    sections = detect_sections(text)

    output_file = os.path.join(
        OUTPUT_FOLDER,
        file_name.replace(".json", "_sections.json")
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as out:

        json.dump(
            sections,
            out,
            indent=4,
            ensure_ascii=False
        )

    print(f"✓ Processed: {file_name}")

print("\nAll resumes processed successfully.")