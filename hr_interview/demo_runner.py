import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from hr_interview.interview_flow import InterviewFlow
from hr_scoring.report_generator import ReportGenerator


class HRInterviewDemoRunner:
    """Builds the final HR interview demo package for stakeholder review."""

    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else ROOT_DIR / "data" / "hr_interview"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _write_json(path, payload):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=4)

    def run(self):
        flow = InterviewFlow().save(experience_level="Experienced", role_type="Technical")
        scoring_report = ReportGenerator.generate()

        demo_dataset = {
            "candidate_profile": {
                "candidate_id": scoring_report.get("candidate_id", "overqualified-001"),
                "role_type": "Technical",
                "experience_level": "Experienced",
                "profile_summary": "Experienced candidate with polished delivery, strong examples, and a structured communication style.",
            },
            "interview_flow": flow,
            "simulated_answers": [
                {
                    "question_id": "INTRO_001",
                    "question": "Tell me about yourself.",
                    "sample_answer": "I am a senior software engineer with seven years of experience building data-driven products and leading cross-functional delivery.",
                },
                {
                    "question_id": "EXP_001",
                    "question": "Tell me about your most recent role.",
                    "sample_answer": "In my most recent role I led a platform team, improved reliability, and mentored engineers while delivering measurable product outcomes.",
                },
                {
                    "question_id": "TECH_001",
                    "question": "Explain a technically challenging project you worked on.",
                    "sample_answer": "I led an ML-driven forecasting initiative that reduced pipeline latency and improved forecasting accuracy through careful experimentation and stable release practices.",
                },
            ],
            "scoring_breakdown": scoring_report.get("score_breakdown", {}),
            "weighted_score": scoring_report.get("weighted_score"),
            "final_hr_score": scoring_report.get("final_hr_score"),
            "recommendation": scoring_report.get("recommendation"),
        }

        manager_feedback = {
            "reviewer": "HR Manager",
            "overall_assessment": "The candidate demonstrates strong role alignment, clear communication, and credible leadership evidence.",
            "strengths": [
                "Clear and structured responses",
                "Strong evidence of ownership and delivery",
                "Good balance between technical depth and interpersonal readiness"
            ],
            "watch_points": [
                "Continue monitoring for overconfidence or overly polished answers",
                "Use a calibration layer for borderline profiles"
            ],
            "recommended_next_step": "Proceed with final interview or hiring decision review.",
        }

        final_demo_report = {
            "status": "ready_for_demo",
            "candidate_id": demo_dataset["candidate_profile"]["candidate_id"],
            "final_score": scoring_report.get("final_hr_score"),
            "final_recommendation": scoring_report.get("recommendation"),
            "architecture_overview": {
                "interview_design": "Role-based question bank with phased HR flow",
                "scoring_logic": "Weighted relevance, communication, confidence, and consistency scores",
                "output_layers": "Interview design, scoring report, candidate recommendation"
            },
            "scoring_logic": {
                "weights": scoring_report.get("weights", {}),
                "components": scoring_report.get("score_breakdown", {})
            },
            "handover_notes": [
                "Interview flow and scoring outputs are generated automatically",
                "Demo dataset is stored for repeatable stakeholder review",
                "Manager feedback is captured for product refinement"
            ],
        }

        self._write_json(self.output_dir / "demo_dataset.json", demo_dataset)
        self._write_json(self.output_dir / "manager_evaluation_feedback.json", manager_feedback)
        self._write_json(self.output_dir / "final_demo_report.json", final_demo_report)

        print("\n========== HR INTERVIEW DEMO READY ==========")
        print(json.dumps(final_demo_report, indent=4))
        print(f"\nArtifacts written to {self.output_dir}")

        return final_demo_report


if __name__ == "__main__":
    HRInterviewDemoRunner().run()
