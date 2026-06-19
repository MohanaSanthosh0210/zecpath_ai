import os
import json
from glob import glob


CONFIG_PATH = "config/eligibility_rules.json"


# =====================================================
# FILE UTILITIES
# =====================================================

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =====================================================
# RULES
# =====================================================

def load_rules():

    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"Rules file not found: {CONFIG_PATH}"
        )

    return load_json(CONFIG_PATH)["default"]


# =====================================================
# SKILLS
# =====================================================

def get_candidate_skills(skill_data):

    skills = []

    for skill in skill_data.get("skills", []):

        skills.append(
            skill.get(
                "normalized_name",
                skill.get("skill_name", "")
            )
        )

    return skills


def calculate_skill_match(
    candidate_skills,
    required_skills
):

    if not required_skills:
        return 100.0, [], []

    candidate_set = {
        s.lower().strip()
        for s in candidate_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower().strip() in candidate_set:
            matched.append(skill)
        else:
            missing.append(skill)

    percentage = (
        len(matched) /
        len(required_skills)
    ) * 100

    return (
        round(percentage, 2),
        matched,
        missing
    )


# =====================================================
# EXPERIENCE
# =====================================================

def get_experience_years(
    experience_data
):
    return experience_data.get(
        "total_experience_years",
        0
    )


def extract_required_experience(
    jd_data
):

    experience_text = str(
        jd_data.get(
            "experience",
            ""
        )
    )

    numbers = []

    current = ""

    for ch in experience_text:

        if ch.isdigit():
            current += ch

        else:

            if current:
                numbers.append(
                    int(current)
                )
                current = ""

    if current:
        numbers.append(int(current))

    return numbers[0] if numbers else 0


# =====================================================
# EDUCATION
# =====================================================

def education_match(jd_data):
    return True


# =====================================================
# ELIGIBILITY EVALUATION
# =====================================================

def evaluate_candidate(
    ats_data,
    skills_data,
    experience_data,
    jd_data,
    rules
):

    ats_score = ats_data.get(
        "final_ats_score",
        ats_data.get(
            "ats_score",
            0
        )
    )

    candidate_skills = (
        get_candidate_skills(
            skills_data
        )
    )

    required_skills = jd_data.get(
        "skills",
        []
    )

    (
        skill_match_percentage,
        matched_skills,
        missing_skills
    ) = calculate_skill_match(
        candidate_skills,
        required_skills
    )

    experience_years = (
        get_experience_years(
            experience_data
        )
    )

    required_experience = (
        extract_required_experience(
            jd_data
        )
    )

    reasons = []

    if (
        ats_score
        >= rules["min_ats_score"]
    ):
        reasons.append(
            "ATS score passed"
        )

    if (
        experience_years
        >= required_experience
    ):
        reasons.append(
            "Experience requirement met"
        )

    if (
        skill_match_percentage
        >= rules[
            "required_skill_match_percentage"
        ]
    ):
        reasons.append(
            f"Skill match {skill_match_percentage}%"
        )

    if education_match(jd_data):
        reasons.append(
            "Education requirement met"
        )

    # ==========================================
    # FINAL DECISION
    # ==========================================

    if (
        ats_score
        >= rules["min_ats_score"]
        and skill_match_percentage
        >= rules[
            "required_skill_match_percentage"
        ]
        and experience_years
        >= required_experience
    ):

        status = "Eligible"

    elif (
        ats_score
        >= rules["review_score"]
    ):

        status = "Review"

    else:

        status = "Rejected"

    return {

        "candidate_id":
            ats_data.get(
                "candidate_id",
                "unknown"
            ),

        "job_id":
            ats_data.get(
                "job_id",
                "unknown"
            ),

        "ats_score":
            round(
                ats_score,
                2
            ),

        "experience_years":
            round(
                experience_years,
                2
            ),

        "required_experience":
            required_experience,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "skill_match_percentage":
            skill_match_percentage,

        "education_match":
            True,

        "eligibility_status":
            status,

        "decision_reason":
            reasons
    }


# =====================================================
# FILE MATCHING
# =====================================================

def find_skill_file(candidate_id):

    candidate_prefix = (
        candidate_id
        .replace("_sections", "")
        .replace("_sectioned", "")
    )

    matches = glob(
        f"data/extracted_skills/{candidate_prefix}*.json"
    )

    return matches[0] if matches else None


def find_experience_file(candidate_id):

    matches = glob(
        f"data/extracted_experience/*{candidate_id}*.json"
    )

    if matches:
        return matches[0]

    candidate_prefix = (
        candidate_id
        .replace("_sections", "")
        .replace("_sectioned", "")
    )

    matches = glob(
        f"data/extracted_experience/*{candidate_prefix}*.json"
    )

    return matches[0] if matches else None


# =====================================================
# RUNNER
# =====================================================

def run_eligibility_engine():

    rules = load_rules()

    ats_files = [

        file

        for file in glob(
            "scoring/ats_scores/*.json"
        )

        if not file.endswith(
            "summary.json"
        )
    ]

    if not ats_files:

        print(
            "No ATS score files found."
        )

        return

    os.makedirs(
        "data/eligibility_results",
        exist_ok=True
    )

    for ats_file in ats_files:

        print(
            f"\nProcessing: {ats_file}"
        )

        ats_data = load_json(
            ats_file
        )

        candidate_id = (
            ats_data.get(
                "candidate_id",
                ""
            )
        )

        job_id = (
            ats_data.get(
                "job_id",
                ""
            )
        )

        skill_file = (
            find_skill_file(
                candidate_id
            )
        )

        experience_file = (
            find_experience_file(
                candidate_id
            )
        )

        jd_file = (
            f"data/structured_jobs/{job_id}.json"
        )

        if not skill_file:

            print(
                f"Skill file not found for {candidate_id}"
            )
            continue

        if not experience_file:

            print(
                f"Experience file not found for {candidate_id}"
            )
            continue

        if not os.path.exists(jd_file):

            print(
                f"JD file not found: {jd_file}"
            )
            continue

        skills_data = load_json(
            skill_file
        )

        experience_data = load_json(
            experience_file
        )

        jd_data = load_json(
            jd_file
        )

        result = evaluate_candidate(
            ats_data,
            skills_data,
            experience_data,
            jd_data,
            rules
        )

        output_file = (
            "data/eligibility_results/"
            f"{candidate_id}_{job_id}.json"
        )

        save_json(
            result,
            output_file
        )

        print(
            f"Saved: {output_file}"
        )

        print(
            f"Status: {result['eligibility_status']}"
        )

    print(
        "\nEligibility processing completed."
    )


if __name__ == "__main__":
    run_eligibility_engine()