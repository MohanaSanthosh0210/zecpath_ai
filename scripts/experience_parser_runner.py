import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parsers.experience_parser import ExperienceParser


def load_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        try:
            from parsers.pdf_reader import extract_text_from_pdf
        except ImportError as error:
            raise ImportError("pdfplumber is required to read PDF resumes. Install it or provide a .json/.txt input file.") from error
        return extract_text_from_pdf(path)
    if ext == ".docx":
        try:
            from parsers.docx_reader import extract_text_from_docx
        except ImportError as error:
            raise ImportError("python-docx is required to read DOCX resumes. Install it or provide a .json/.txt input file.") from error
        return extract_text_from_docx(path)
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            if "cleaned_text" in data or "text" in data:
                return data.get("cleaned_text") or data.get("text") or ""
            if "experience" in data:
                experience_section = data.get("experience")
                if isinstance(experience_section, list):
                    return "\n\n".join(experience_section)
                if isinstance(experience_section, str):
                    return experience_section

        return ""

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def find_resume_candidates() -> list:
    resume_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "resumes"))
    supported = [".pdf", ".docx", ".txt"]
    candidates = []

    if os.path.isdir(resume_dir):
        candidates.extend(
            os.path.join(resume_dir, filename)
            for filename in sorted(os.listdir(resume_dir))
            if os.path.splitext(filename)[1].lower() in supported
        )

    return candidates


def find_sectioned_resume_candidates() -> list:
    sectioned_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "sectioned_resumes"))
    candidates = []

    if os.path.isdir(sectioned_dir):
        candidates.extend(
            os.path.join(sectioned_dir, filename)
            for filename in sorted(os.listdir(sectioned_dir))
            if os.path.splitext(filename)[1].lower() == ".json"
        )

    return candidates


def find_default_resume() -> str:
    candidates = find_resume_candidates()
    if not candidates:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        raise FileNotFoundError(
            f"No supported resume file found in {os.path.join(base_dir, 'data', 'cleaned')} or {os.path.join(base_dir, 'data', 'resumes')}"
        )
    return candidates[0]


def main():
    parser = argparse.ArgumentParser(
        description="Parse resume experience and save structured JSON output."
    )
    parser.add_argument(
        "--input",
        help="Path to a resume file. If omitted, the first file in data/resumes is used.",
        default=None,
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save the JSON output file.",
        default="data/extracted_experience",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all supported resumes in data/resumes.",
    )
    parser.add_argument(
        "--sectioned",
        action="store_true",
        help="Process all sectioned resume JSON files in data/sectioned_resumes.",
    )
    args = parser.parse_args()

    if args.input:
        resume_paths = [args.input]
    elif args.sectioned:
        resume_paths = find_sectioned_resume_candidates()
        if not resume_paths:
            raise FileNotFoundError("No sectioned resume files found to process.")
        print(f"Processing {len(resume_paths)} sectioned resume files...")
    elif args.all:
        resume_paths = find_resume_candidates()
        if not resume_paths:
            raise FileNotFoundError("No supported resume files found to process.")
        print(f"Processing {len(resume_paths)} resume files...")
    else:
        resume_paths = [find_default_resume()]
        print(f"Using default resume file: {resume_paths[0]}")

    experience_parser = ExperienceParser()
    for resume_path in resume_paths:
        resume_text = load_text_from_file(resume_path)
        experience_data = experience_parser.extract_experience(resume_text)
        name = os.path.splitext(os.path.basename(resume_path))[0]
        ext = os.path.splitext(resume_path)[1].lstrip(".")
        if args.sectioned:
            output_filename = f"{name}_sectioned_experience.json"
        else:
            output_filename = f"{name}_{ext}_experience.json"
        output_path = experience_parser.save_experience_json(
            experience_data,
            output_dir=args.output_dir,
            filename=output_filename,
        )
        print(f"Saved experience JSON to: {output_path}")


if __name__ == "__main__":
    main()
