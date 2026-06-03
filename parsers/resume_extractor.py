import os
import sys
import json

sys.path.append(os.path.abspath("."))

from pdf_reader import extract_text_from_pdf
from docx_reader import extract_text_from_docx
from text_cleaner import clean_resume_text
from utils.logger import get_logger

logger = get_logger(__name__)

INPUT_FOLDER = "data/resumes"
OUTPUT_FOLDER = "data/cleaned"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_resume(file_path):

    raw_text = ""

    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)

    cleaned_text = clean_resume_text(raw_text)

    return {
        "file_name": os.path.basename(file_path),
        "cleaned_text": cleaned_text
    }

for file in os.listdir(INPUT_FOLDER):

    file_path = os.path.join(INPUT_FOLDER, file)

    result = process_resume(file_path)

    output_file = os.path.join(
        OUTPUT_FOLDER,
        file.split(".")[0] + ".json"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    logger.info(f"Processed Resume: {file}")

    print(f"Processed: {file}")