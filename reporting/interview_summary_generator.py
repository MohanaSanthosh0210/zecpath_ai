import os
from typing import Any, Dict, List, Optional

from reporting.report_utils import load_json, save_json


class InterviewSummaryGenerator:
    """Build recruiter-ready interview summaries from AI analysis outputs."""

    def __init__(self, output_dir: str = "data/interview_summaries"):
        self.output_dir = output_dir

    @staticmethod
    def _get_candidate_id(answer_data: Dict[str, Any], hr_score_data: Optional[Dict[str, Any]] = None) -> str:
        if hr_score_data and hr_score_data.get("candidate_id"):
            return str(hr_score_data["candidate_id"])
        if answer_data.get("candidate_id"):
            return str(answer_data["candidate_id"])
        return "UNKNOWN"

    @staticmethod
    def _normalize_score(value: Optional[float]) -> float:
        try:
            return round(float(value or 0), 2)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _recommendation(score: float) -> str:
        if score >= 85:
            return "Strong Hire"
        if score >= 70:
            return "Hire"
        if score >= 60:
            return "Review"
        return "Reject"

    def _build_strengths(
        self,
        answer_data: Dict[str, Any],
        communication_data: Dict[str, Any],
        behavior_data: Dict[str, Any],
        hr_score_data: Dict[str, Any],
    ) -> List[str]:
        strengths: List[str] = []
        communication_score = self._normalize_score(
            communication_data.get("communication_score")
        )
        confidence_score = self._normalize_score(
            behavior_data.get("confidence", {}).get("confidence_score")
        )
        sentiment = (
            behavior_data.get("sentiment", {}).get("sentiment", "Neutral")
        )
        skills = answer_data.get("skills") or []
        experience = answer_data.get("experience")
        normalized_score = self._normalize_score(
            hr_score_data.get("normalized_score")
        )

        if communication_score >= 85:
            strengths.append("Strong verbal communication and clarity")
        if confidence_score >= 80:
            strengths.append("Confident and composed delivery")
        if skills:
            strengths.append("Relevant technical skills were demonstrated")
        if experience:
            strengths.append(f"Experience was clearly referenced ({experience})")
        if sentiment == "Positive":
            strengths.append("Positive interview demeanor")
        if normalized_score >= 70:
            strengths.append("Overall interview performance met the hiring threshold")

        return strengths

    def _build_weaknesses(
        self,
        answer_data: Dict[str, Any],
        communication_data: Dict[str, Any],
        behavior_data: Dict[str, Any],
        hr_score_data: Dict[str, Any],
    ) -> List[str]:
        weaknesses: List[str] = []
        communication_score = self._normalize_score(
            communication_data.get("communication_score")
        )
        confidence_score = self._normalize_score(
            behavior_data.get("confidence", {}).get("confidence_score")
        )
        normalized_score = self._normalize_score(
            hr_score_data.get("normalized_score")
        )
        structured_answer = answer_data.get("structured_answer", {})

        if communication_score < 80:
            weaknesses.append("Communication clarity needs improvement")
        if confidence_score < 60:
            weaknesses.append("Confidence levels appeared limited during the interview")
        if answer_data.get("missing_details"):
            weaknesses.append("Some answers lacked important detail")
        if answer_data.get("off_topic"):
            weaknesses.append("Some responses were not fully on-topic")
        if answer_data.get("salary_expectation") is None:
            weaknesses.append("Compensation expectations were not clarified")
        if answer_data.get("availability") is None:
            weaknesses.append("Availability details were not provided")
        if structured_answer.get("intent_confidence", 0) < 0.6:
            weaknesses.append("Intent confidence for some answers was modest")
        if normalized_score < 60:
            weaknesses.append("Overall HR performance was below the target range")

        return weaknesses

    def _build_cultural_fit_indicators(
        self,
        answer_data: Dict[str, Any],
        communication_data: Dict[str, Any],
        behavior_data: Dict[str, Any],
    ) -> List[str]:
        indicators: List[str] = []
        communication_score = self._normalize_score(
            communication_data.get("communication_score")
        )
        sentiment = (
            behavior_data.get("sentiment", {}).get("sentiment", "Neutral")
        )
        contradictions = behavior_data.get("contradictions", {}).get("count", 0)

        if communication_score >= 85:
            indicators.append("Communication style appears collaborative and professional")
        if sentiment in {"Positive", "Neutral"}:
            indicators.append("Interview tone suggests professionalism and composure")
        if contradictions == 0:
            indicators.append("Responses were consistent and low-risk from a behavioral standpoint")
        if answer_data.get("skills"):
            indicators.append("The candidate appears aligned with the role’s core skill requirements")

        return indicators

    def _build_risk_flags(
        self,
        answer_data: Dict[str, Any],
        behavior_data: Dict[str, Any],
        hr_score_data: Dict[str, Any],
    ) -> List[str]:
        risks: List[str] = []
        if answer_data.get("off_topic"):
            risks.append("Responses included off-topic content")
        if answer_data.get("missing_details"):
            risks.append("Important detail was missing in some responses")
        if answer_data.get("salary_expectation") is None:
            risks.append("Salary expectations were not surfaced")
        if answer_data.get("availability") is None:
            risks.append("Work availability was not clarified")
        contradictions = behavior_data.get("contradictions", {}).get("count", 0)
        if contradictions > 0:
            risks.append("Behavioral analysis detected response contradictions")
        normalized_score = self._normalize_score(
            hr_score_data.get("normalized_score")
        )
        if normalized_score < 60:
            risks.append("Overall HR score falls below the recommended hire threshold")

        return risks

    def _build_inconsistencies(
        self,
        answer_data: Dict[str, Any],
        communication_data: Dict[str, Any],
        behavior_data: Dict[str, Any],
    ) -> List[str]:
        inconsistencies: List[str] = []
        communication_score = self._normalize_score(
            communication_data.get("communication_score")
        )
        confidence_score = self._normalize_score(
            behavior_data.get("confidence", {}).get("confidence_score")
        )
        structured_answer = answer_data.get("structured_answer", {})

        if communication_score >= 85 and confidence_score < 70:
            inconsistencies.append("The candidate sounded polished but showed lower confidence than expected")
        if answer_data.get("off_topic") and not answer_data.get("missing_details"):
            inconsistencies.append("The candidate provided a direct answer but drifted off-topic in places")
        if structured_answer.get("intent_confidence", 0) < 0.6 and answer_data.get("skills"):
            inconsistencies.append("The technical profile appeared strong, but intent detection was less certain")
        if behavior_data.get("sentiment", {}).get("sentiment") == "Neutral" and confidence_score >= 80:
            inconsistencies.append("The candidate appeared confident, yet the tone remained neutral")

        return inconsistencies

    def _build_overall_hr_performance(
        self,
        hr_score_data: Dict[str, Any],
        strengths: List[str],
        weaknesses: List[str],
        risks: List[str],
    ) -> Dict[str, Any]:
        score = self._normalize_score(hr_score_data.get("normalized_score"))
        summary = (
            "The candidate delivered a solid interview performance with "
            f"{len(strengths)} strengths and {len(weaknesses)} areas to improve."
        )
        if risks:
            summary += f" Key risks include: {'; '.join(risks[:2])}."

        return {
            "score": score,
            "recommendation": self._recommendation(score),
            "summary": summary,
            "strengths_count": len(strengths),
            "risk_count": len(risks),
        }

    def _build_natural_language_report(
        self,
        candidate_id: str,
        strengths: List[str],
        weaknesses: List[str],
        cultural_fit_indicators: List[str],
        risks: List[str],
        inconsistencies: List[str],
        overall_performance: Dict[str, Any],
    ) -> str:
        strength_text = "; ".join(strengths) if strengths else "No notable strengths were detected"
        weakness_text = "; ".join(weaknesses) if weaknesses else "No major weaknesses were identified"
        fit_text = "; ".join(cultural_fit_indicators) if cultural_fit_indicators else "Fit indicators were limited"
        risk_text = "; ".join(risks) if risks else "No critical risks were detected"
        inconsistency_text = "; ".join(inconsistencies) if inconsistencies else "No major inconsistencies were detected"
        return (
            f"Candidate {candidate_id} showed a balanced interview profile. "
            f"Strengths include {strength_text}. "
            f"Weaknesses include {weakness_text}. "
            f"Cultural fit indicators suggest {fit_text}. "
            f"Risk flags include {risk_text}. "
            f"Inconsistencies noted: {inconsistency_text}. "
            f"Overall HR performance is {overall_performance['score']}/100 with a recommendation of {overall_performance['recommendation']}."
        )

    def generate_report(
        self,
        answer_data: Optional[Dict[str, Any]] = None,
        communication_data: Optional[Dict[str, Any]] = None,
        behavior_data: Optional[Dict[str, Any]] = None,
        hr_score_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        answer_data = answer_data or {}
        communication_data = communication_data or {}
        behavior_data = behavior_data or {}
        hr_score_data = hr_score_data or {}

        candidate_id = self._get_candidate_id(answer_data, hr_score_data)
        strengths = self._build_strengths(
            answer_data,
            communication_data,
            behavior_data,
            hr_score_data,
        )
        weaknesses = self._build_weaknesses(
            answer_data,
            communication_data,
            behavior_data,
            hr_score_data,
        )
        cultural_fit = self._build_cultural_fit_indicators(
            answer_data,
            communication_data,
            behavior_data,
        )
        risks = self._build_risk_flags(answer_data, behavior_data, hr_score_data)
        inconsistencies = self._build_inconsistencies(
            answer_data,
            communication_data,
            behavior_data,
        )
        overall_performance = self._build_overall_hr_performance(
            hr_score_data,
            strengths,
            weaknesses,
            risks,
        )

        report = {
            "candidate_id": candidate_id,
            "candidate_strengths": strengths,
            "candidate_weaknesses": weaknesses,
            "cultural_fit_indicators": cultural_fit,
            "risk_flags": risks,
            "inconsistencies": inconsistencies,
            "overall_hr_performance": overall_performance,
            "natural_language_report": self._build_natural_language_report(
                candidate_id,
                strengths,
                weaknesses,
                cultural_fit,
                risks,
                inconsistencies,
                overall_performance,
            ),
        }
        return report

    def generate_and_save(
        self,
        answer_data: Optional[Dict[str, Any]] = None,
        communication_data: Optional[Dict[str, Any]] = None,
        behavior_data: Optional[Dict[str, Any]] = None,
        hr_score_data: Optional[Dict[str, Any]] = None,
        output_file: Optional[str] = None,
    ) -> Dict[str, Any]:
        report = self.generate_report(
            answer_data=answer_data,
            communication_data=communication_data,
            behavior_data=behavior_data,
            hr_score_data=hr_score_data,
        )
        os.makedirs(self.output_dir, exist_ok=True)
        target_file = output_file or os.path.join(
            self.output_dir,
            f"{report['candidate_id']}_summary.json",
        )
        save_json(report, target_file)
        return report


if __name__ == "__main__":
    generator = InterviewSummaryGenerator()
    answer_data = load_json("data/understood_answers/sample_answer.json")
    communication_data = load_json("data/communication/communication_score.json")
    behavior_data = load_json("data/behavioral_analysis/behavioral_report.json")
    hr_score_data = load_json("data/hr_scoring/hr_score_report.json")
    report = generator.generate_and_save(
        answer_data=answer_data,
        communication_data=communication_data,
        behavior_data=behavior_data,
        hr_score_data=hr_score_data,
    )
    print(report["natural_language_report"])
