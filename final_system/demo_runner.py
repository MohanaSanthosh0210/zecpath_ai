import json
import os

from final_system.system_pipeline import AIScreeningPipeline
from scoring.unified_scoring_engine import calculate_unified_score


def build_unified_candidate_report(data, role=None, candidate_id=None, job_id=None):
    understood = data.get("understood_answer") or {}
    screening = data.get("screening_score") or {}
    behavior = data.get("behavior_report") or {}
    report = data.get("screening_report") or {}
    conversation = data.get("conversation") or {}
    edge = data.get("edge_case") or {}
    hr_score_data = data.get("hr_score") or {}

    ats_score = data.get("ats_score", 0)
    screening_score = screening.get("final_screening_score", 0)
    hr_score = hr_score_data.get("final_hr_score", 0)

    unified_score = calculate_unified_score(
        role=role or understood.get("intent") or "",
        ats_score=ats_score,
        screening_score=screening_score,
        hr_score=hr_score,
        candidate_id=candidate_id,
        job_id=job_id,
    )

    return {
        "candidate": {
            "intent": understood.get("intent"),
            "skills": understood.get("skills"),
            "experience": understood.get("experience"),
        },
        "screening": {
            "score": screening.get("final_screening_score"),
            "status": screening.get("status"),
        },
        "behavior": behavior,
        "screening_report": report,
        "conversation": conversation,
        "edge_case": edge,
        "unified_candidate_score": unified_score,
    }


class DemoRunner:

    OUTPUT_FILE = (

        "data/final_demo/demo_output.json"

    )

    def run(self):

        pipeline = AIScreeningPipeline()

        data = pipeline.run()

        # -----------------------------
        # Candidate Summary
        # -----------------------------

        final_result = build_unified_candidate_report(
            data,
            role=(data.get("understood_answer") or {}).get("intent"),
            candidate_id=None,
            job_id=None,
        )

        os.makedirs(

            "data/final_demo",

            exist_ok=True

        )

        with open(

            self.OUTPUT_FILE,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                final_result,

                file,

                indent=4

            )

        print(

            "\n========== AI SCREENING DEMO ==========\n"

        )

        print(

            json.dumps(

                final_result,

                indent=4

            )

        )

        print(

            "\nDemo saved to "

            "data/final_demo/demo_output.json"

        )


if __name__ == "__main__":

    DemoRunner().run()