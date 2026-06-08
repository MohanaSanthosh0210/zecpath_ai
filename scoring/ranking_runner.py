import json
import os

from scoring.ranking_engine import rank_candidates

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ATS_SCORES_DIR = os.path.join(ROOT_DIR, "scoring", "ats_scores")
OUTPUT_DIR = os.path.join(ROOT_DIR, "scoring", "ranking_outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_candidate_scores():
    """
    Load ATS score files and skip summary.json.
    """

    candidates = []

    if not os.path.exists(ATS_SCORES_DIR):
        print(f"ATS score directory not found: {ATS_SCORES_DIR}")
        return candidates

    for file_name in os.listdir(ATS_SCORES_DIR):

        # only candidate score files
        if not file_name.endswith(".json"):
            continue

        if file_name == "summary.json":
            continue

        file_path = os.path.join(ATS_SCORES_DIR, file_name)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # skip malformed files
            if "candidate_id" not in data:
                continue

            candidates.append(data)

        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    return candidates


def classify_candidate(score):
    """
    Day 14 zones
    """

    if score >= 75:
        return "Shortlisted"

    if score >= 50:
        return "Review"

    return "Rejected"


def build_recruiter_view(candidates):
    """
    Recruiter-friendly output
    """

    recruiter_view = []

    for rank, candidate in enumerate(candidates, start=1):

        recruiter_view.append(
            {
                "rank": rank,
                "candidate_id": candidate["candidate_id"],
                "job_id": candidate["job_id"],
                "ats_score": candidate["final_ats_score"],
                "status": candidate["status"],
                "skills_score": candidate["skill_score"],
                "experience_score": candidate["experience_score"],
                "education_score": candidate["education_score"],
                "semantic_score": candidate["semantic_score"],
                "reason": candidate["reason"],
            }
        )

    return recruiter_view


def save_json(file_name, data):

    output_path = os.path.join(OUTPUT_DIR, file_name)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved: {output_path}")


def main():

    candidates = load_candidate_scores()

    if not candidates:
        print("No ATS candidate files found.")
        return

    print(f"\nLoaded {len(candidates)} candidates\n")

    # -------------------------
    # Rank candidates
    # -------------------------

    ranked_candidates = rank_candidates(candidates)

    # -------------------------
    # Assign ranking zones
    # -------------------------

    for rank, candidate in enumerate(ranked_candidates, start=1):

        candidate["rank"] = rank

        candidate["ranking_zone"] = classify_candidate(
            candidate["final_ats_score"]
        )

    # -------------------------
    # Shortlisted candidates
    # -------------------------

    shortlisted_candidates = [
        c
        for c in ranked_candidates
        if c["ranking_zone"] == "Shortlisted"
    ]

    # -------------------------
    # Recruiter view
    # -------------------------

    recruiter_view = build_recruiter_view(
        ranked_candidates
    )

    # -------------------------
    # Save outputs
    # -------------------------

    save_json(
        "ranked_candidates.json",
        ranked_candidates
    )

    save_json(
        "shortlisted_candidates.json",
        shortlisted_candidates
    )

    save_json(
        "recruiter_view.json",
        recruiter_view
    )

    print("\nRanking Complete\n")

    print(
        f"Total Candidates : {len(ranked_candidates)}"
    )

    print(
        f"Shortlisted      : {len(shortlisted_candidates)}"
    )


if __name__ == "__main__":
    main()