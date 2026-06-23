# tests/test_day24_pipeline.py

from pathlib import Path

from transcripts.transcript_cleaner import (
    clean_transcript
)

from transcripts.transcript_normalizer import (
    normalize_transcript
)


RAW_FOLDER = Path(
    "transcripts/raw_transcripts"
)

OUTPUT_FOLDER = Path(
    "transcripts/cleaned_transcripts"
)

OUTPUT_FOLDER.mkdir(
    exist_ok=True
)

for file in RAW_FOLDER.glob("*.txt"):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        raw_text = f.read()

    cleaned = clean_transcript(
        raw_text
    )

    normalized = normalize_transcript(
        cleaned
    )

    output_file = (
        OUTPUT_FOLDER /
        file.name.replace(
            "_raw",
            "_clean"
        )
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(normalized)

    print(
        f"Saved: {output_file}"
    )

print(
    "\nDay 24 Pipeline Completed"
)