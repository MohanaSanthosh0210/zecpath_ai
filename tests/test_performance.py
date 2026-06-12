import os
import time

from parsers.docx_reader import DocumentReader
from skills.skill_extractor import SkillExtractor
from parsers.education_parser import EducationParser
from parsers.experience_parser import ExperienceParser


reader = DocumentReader()
skill_extractor = SkillExtractor()
education_parser = EducationParser()
experience_parser = ExperienceParser()

RESUME_FOLDER = "data/resumes"

print("\n======================================")
print("ZECPATH PERFORMANCE BENCHMARK")
print("======================================\n")

results = []

for file in os.listdir(RESUME_FOLDER):

    if not (
        file.endswith(".pdf")
        or file.endswith(".docx")
    ):
        continue

    resume_path = os.path.join(
        RESUME_FOLDER,
        file
    )

    print(f"\nProcessing: {file}")

    pipeline_start = time.time()

    # -------------------------
    # Resume Reading
    # -------------------------
    start = time.time()

    resume_text = reader.extract_text(
        resume_path
    )

    read_time = time.time() - start

    # -------------------------
    # Skill Extraction
    # -------------------------
    start = time.time()

    skills = skill_extractor.extract_skills(
        resume_text
    )

    skill_time = time.time() - start

    # -------------------------
    # Education Parsing
    # -------------------------
    start = time.time()

    education = education_parser.extract_education(
        resume_text
    )

    education_time = time.time() - start

    # -------------------------
    # Experience Parsing
    # -------------------------
    start = time.time()

    experience = experience_parser.extract_experience(
        resume_text
    )

    experience_time = time.time() - start

    total_time = (
        time.time()
        - pipeline_start
    )

    results.append({

        "resume": file,

        "read_time":
            round(read_time, 4),

        "skill_time":
            round(skill_time, 4),

        "education_time":
            round(education_time, 4),

        "experience_time":
            round(experience_time, 4),

        "total_time":
            round(total_time, 4),

        "skills_found":
            len(skills),

        "education_entries":
            len(
                education.get(
                    "education_items",
                    []
                )
            ),

        "experience_entries":
            len(
                experience.get(
                    "experience_items",
                    []
                )
            )
    })


# ==================================
# FINAL REPORT
# ==================================

print("\n\n======================================")
print("FINAL PERFORMANCE REPORT")
print("======================================")

for r in results:

    print("\n--------------------------------")

    print(
        f"Resume: {r['resume']}"
    )

    print(
        f"Read Time        : {r['read_time']} sec"
    )

    print(
        f"Skill Time       : {r['skill_time']} sec"
    )

    print(
        f"Education Time   : {r['education_time']} sec"
    )

    print(
        f"Experience Time  : {r['experience_time']} sec"
    )

    print(
        f"Total Time       : {r['total_time']} sec"
    )

    print(
        f"Skills Found     : {r['skills_found']}"
    )

    print(
        f"Education Items  : {r['education_entries']}"
    )

    print(
        f"Experience Items : {r['experience_entries']}"
    )


avg_time = sum(
    r["total_time"]
    for r in results
) / len(results)

print("\n======================================")
print(
    f"Average Pipeline Time: {avg_time:.4f} sec"
)
print("======================================")