import json
import os

from screening.scoring_engine import ScreeningScoringEngine


STRUCTURED_ANSWER_DIR = "data/understood_answers"
QUESTION_SCORE_DIR = "data/screening_scores/question_scores"
FINAL_SCORE_DIR = "data/screening_scores/final_scores"


os.makedirs(QUESTION_SCORE_DIR, exist_ok=True)
os.makedirs(FINAL_SCORE_DIR, exist_ok=True)


def aggregate_scores():

    engine = ScreeningScoringEngine()

    candidate_scores = {}

    candidate_breakdowns = {}

    for file_name in os.listdir(STRUCTURED_ANSWER_DIR):
        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(STRUCTURED_ANSWER_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            answer_data = json.load(file)

        score_result = engine.score_answer(answer_data)

        question_output_path = os.path.join(QUESTION_SCORE_DIR, file_name)
        with open(question_output_path, "w", encoding="utf-8") as file:
            json.dump(score_result, file, indent=4)

        candidate_id = answer_data.get("candidate_id") or "unknown"
        candidate_scores.setdefault(candidate_id, []).append(score_result["final_score"])
        candidate_breakdowns.setdefault(candidate_id, []).append(score_result)

    for candidate_id, scores in candidate_scores.items():
        breakdowns = candidate_breakdowns[candidate_id]
        question_count = len(scores)
        final_score = round(sum(scores) / question_count, 2)

        component_totals = {
            "clarity": 0.0,
            "relevance": 0.0,
            "completeness": 0.0,
            "consistency": 0.0
        }

        for detail in breakdowns:
            component_totals["clarity"] += detail["clarity"]
            component_totals["relevance"] += detail["relevance"]
            component_totals["completeness"] += detail["completeness"]
            component_totals["consistency"] += detail["consistency"]

        average_component_scores = {
            key: round(total / question_count, 2)
            for key, total in component_totals.items()
        }

        result = {
            "candidate_id": candidate_id,
            "question_count": question_count,
            "question_scores": scores,
            "question_breakdown": breakdowns,
            "average_component_scores": average_component_scores,
            "final_screening_score": final_score,
            "status": "Pass" if final_score >= 75 else "Review"
        }

        output_file = os.path.join(
            FINAL_SCORE_DIR,
            f"{candidate_id}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                result,
                file,
                indent=4
            )

        print(
            f"Processed Candidate: "
            f"{candidate_id}"
        )


if __name__ == "__main__":
    aggregate_scores()