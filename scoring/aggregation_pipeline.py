"""Comprehensive integration pipeline for cross-round aggregation."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from schemas.unified_candidate_score import UnifiedCandidateScore, RoundScore
from scoring.cross_round_aggregation import (
    CrossRoundAggregationEngine,
    HiringFitCalculator,
)


class CrossRoundScoringPipeline:
    """
    Complete pipeline for candidate evaluation and hiring fit calculation.
    
    Workflow:
    1. Collect scores from all evaluation stages
    2. Apply role-specific weightage
    3. Normalize scores for comparison
    4. Calculate unified hiring intelligence score
    5. Generate transparent scoring breakdown
    6. Produce hiring recommendations
    """
    
    def __init__(self, custom_weights: Optional[Dict[str, Dict[str, float]]] = None):
        """Initialize the pipeline."""
        self.engine = CrossRoundAggregationEngine(custom_weights)
        self.calculator = HiringFitCalculator()
        self.results = []
    
    def process_candidate(
        self,
        candidate_id: str,
        role: str,
        ats_score: Optional[float] = None,
        screening_score: Optional[float] = None,
        hr_interview_score: Optional[float] = None,
        technical_interview_score: Optional[float] = None,
        machine_test_score: Optional[float] = None,
        behavioral_intelligence_score: Optional[float] = None,
        job_id: Optional[str] = None,
        **additional_data,
    ) -> UnifiedCandidateScore:
        """
        Process a single candidate through the complete pipeline.
        
        Args:
            candidate_id: Unique candidate identifier
            role: Job role/position
            ats_score: ATS/resume screening score (0-100)
            screening_score: Initial screening/phone screen score
            hr_interview_score: HR interview score
            technical_interview_score: Technical interview score
            machine_test_score: Machine test/coding challenge score
            behavioral_intelligence_score: Behavioral/personality score
            job_id: Optional job identifier
            **additional_data: Any additional candidate data
            
        Returns:
            UnifiedCandidateScore with complete breakdown
        """
        scores = {
            "ats": ats_score,
            "screening": screening_score,
            "hr_interview": hr_interview_score,
            "technical_interview": technical_interview_score,
            "machine_test": machine_test_score,
            "behavioral_intelligence": behavioral_intelligence_score,
        }

        for key in ["ats", "screening", "hr_interview", "technical_interview", "machine_test", "behavioral_intelligence"]:
            if scores.get(key) is None and key in additional_data:
                scores[key] = additional_data.get(key)
        
        # Remove None values
        scores = {k: v for k, v in scores.items() if v is not None}
        
        # Aggregate
        unified_score = self.engine.aggregate(
            candidate_id=candidate_id,
            role=role,
            scores=scores,
            job_id=job_id,
            normalize=True,
            detect_outliers=True,
        )
        
        # Store result
        self.results.append(unified_score)
        
        return unified_score
    
    def process_batch(
        self,
        candidates: List[Dict[str, Any]],
    ) -> List[UnifiedCandidateScore]:
        """
        Process multiple candidates.
        
        Args:
            candidates: List of candidate data dictionaries
            
        Returns:
            List of UnifiedCandidateScore objects
        """
        results = []
        for candidate_data in candidates:
            candidate_id = candidate_data.pop("candidate_id", "")
            role = candidate_data.pop("role", "")
            job_id = candidate_data.pop("job_id", None)
            
            result = self.process_candidate(
                candidate_id=candidate_id,
                role=role,
                job_id=job_id,
                **candidate_data,
            )
            results.append(result)
        
        return results
    
    def generate_comparison_report(
        self,
        candidates: Optional[List[UnifiedCandidateScore]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a comparison report for multiple candidates.
        
        Args:
            candidates: Optional list of candidates (defaults to pipeline results)
            
        Returns:
            Comparison report with rankings and insights
        """
        candidates_to_compare = candidates or self.results
        
        if not candidates_to_compare:
            return {"error": "No candidates to compare"}
        
        # Sort by hiring fit
        sorted_candidates = sorted(
            candidates_to_compare,
            key=lambda x: x.hiring_fit_percentage,
            reverse=True,
        )
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "total_candidates": len(sorted_candidates),
            "candidates": [],
            "statistics": self._calculate_statistics(sorted_candidates),
            "recommendations": self._generate_recommendations(sorted_candidates),
        }
        
        # Add each candidate to report
        for rank, candidate in enumerate(sorted_candidates, 1):
            report["candidates"].append({
                "rank": rank,
                "candidate_id": candidate.candidate_id,
                "role": candidate.role,
                "hiring_fit_percentage": candidate.hiring_fit_percentage,
                "status": candidate.status.value,
                "decision": candidate.decision,
                "recommendation": candidate.recommendation,
                "strengths": candidate.strengths[:3],  # Top 3
                "concerns": candidate.concerns[:3],    # Top 3
                "red_flags": candidate.red_flags,
                "missing_rounds": candidate.missing_rounds,
            })
        
        return report
    
    def _calculate_statistics(
        self,
        candidates: List[UnifiedCandidateScore],
    ) -> Dict[str, Any]:
        """Calculate statistics across candidates."""
        if not candidates:
            return {}
        
        fit_scores = [c.hiring_fit_percentage for c in candidates]
        
        return {
            "average_fit_score": round(sum(fit_scores) / len(fit_scores), 2),
            "median_fit_score": sorted(fit_scores)[len(fit_scores) // 2],
            "min_fit_score": min(fit_scores),
            "max_fit_score": max(fit_scores),
            "std_deviation": self._calculate_std_dev(fit_scores),
            "distribution_by_status": self._count_by_status(candidates),
        }
    
    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return round(variance ** 0.5, 2)
    
    def _count_by_status(self, candidates: List[UnifiedCandidateScore]) -> Dict[str, int]:
        """Count candidates by status."""
        status_counts = {}
        for candidate in candidates:
            status = candidate.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts
    
    def _generate_recommendations(
        self,
        sorted_candidates: List[UnifiedCandidateScore],
    ) -> List[str]:
        """Generate hiring recommendations."""
        recommendations = []
        
        # Strong fit candidates
        strong_fit = [c for c in sorted_candidates if c.decision == "APPROVE"]
        if strong_fit:
            recommendations.append(
                f"Recommend proceeding with {len(strong_fit)} strong candidate(s): "
                f"{', '.join(c.candidate_id for c in strong_fit[:3])}"
            )
        
        # Review candidates
        review = [c for c in sorted_candidates if c.decision == "REVIEW"]
        if review:
            recommendations.append(
                f"Schedule additional interviews for {len(review)} candidate(s)"
            )
        
        # No fit candidates
        no_fit = [c for c in sorted_candidates if c.decision == "REJECT"]
        if no_fit:
            recommendations.append(
                f"{len(no_fit)} candidate(s) do not meet role requirements"
            )
        
        if not recommendations:
            recommendations.append("No clear recommendations at this time")
        
        return recommendations
    
    def export_results(self, filepath: str, format: str = "json") -> None:
        """
        Export results to file.
        
        Args:
            filepath: Path to export file
            format: Format (json, csv)
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            data = [r.to_dict() for r in self.results]
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
        
        elif format == "csv":
            import csv
            if not self.results:
                return
            
            fieldnames = [
                "candidate_id",
                "role",
                "hiring_fit_percentage",
                "status",
                "decision",
                "ats_score",
                "screening_score",
                "hr_interview_score",
                "technical_interview_score",
                "machine_test_score",
            ]
            
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in self.results:
                    row = {
                        "candidate_id": result.candidate_id,
                        "role": result.role,
                        "hiring_fit_percentage": result.hiring_fit_percentage,
                        "status": result.status.value,
                        "decision": result.decision,
                    }
                    
                    # Add round scores
                    for round_name, round_score in result.round_scores.items():
                        row[f"{round_name}_score"] = round_score.score
                    
                    writer.writerow(row)
    
    def clear_results(self) -> None:
        """Clear stored results."""
        self.results = []


class AggregationReportGenerator:
    """Generate detailed aggregation reports."""
    
    @staticmethod
    def generate_candidate_report(
        unified_score: UnifiedCandidateScore,
    ) -> str:
        """Generate a detailed report for a single candidate."""
        report = []
        report.append("=" * 70)
        report.append("HIRING INTELLIGENCE REPORT - CROSS-ROUND AGGREGATION")
        report.append("=" * 70)
        report.append("")
        
        # Header
        report.append(f"Candidate ID: {unified_score.candidate_id}")
        report.append(f"Role: {unified_score.role}")
        report.append(f"Job ID: {unified_score.job_id or 'N/A'}")
        report.append(f"Assessment Date: {unified_score.calculation_timestamp}")
        report.append("")
        
        # Overall Score
        report.append("OVERALL HIRING FIT SCORE")
        report.append("-" * 70)
        report.append(f"Hiring Fit: {unified_score.hiring_fit_percentage}%")
        report.append(f"Status: {unified_score.status.value}")
        report.append(f"Decision: {unified_score.decision}")
        report.append(f"Recommendation: {unified_score.recommendation}")
        report.append("")
        
        # Round Scores
        report.append("ROUND-WISE SCORES")
        report.append("-" * 70)
        for round_name, round_score in unified_score.round_scores.items():
            report.append(f"{round_name.upper()}:")
            report.append(f"  Score: {round_score.score}/100")
            report.append(f"  Normalized: {round_score.normalized_score:.2f}")
            report.append(f"  Weight: {round_score.weight:.1%}")
            report.append(f"  Contribution: {round_score.weighted_contribution:.2f}")
            report.append("")
        
        # Weights
        report.append("WEIGHTAGE APPLIED")
        report.append("-" * 70)
        weights = unified_score.weights.to_dict()
        for round_name, weight in weights.items():
            if weight > 0:
                report.append(f"  {round_name}: {weight:.1%}")
        report.append("")
        
        # Component Contributions
        report.append("COMPONENT CONTRIBUTIONS")
        report.append("-" * 70)
        for round_name, contribution in unified_score.component_contributions.items():
            bar = "█" * int(contribution / 2)
            report.append(f"  {round_name:20s}: {contribution:6.2f}% {bar}")
        report.append("")
        
        # Strengths
        if unified_score.strengths:
            report.append("STRENGTHS")
            report.append("-" * 70)
            for i, strength in enumerate(unified_score.strengths, 1):
                report.append(f"  {i}. {strength}")
            report.append("")
        
        # Concerns
        if unified_score.concerns:
            report.append("CONCERNS")
            report.append("-" * 70)
            for i, concern in enumerate(unified_score.concerns, 1):
                report.append(f"  {i}. {concern}")
            report.append("")
        
        # Red Flags
        if unified_score.red_flags:
            report.append("RED FLAGS")
            report.append("-" * 70)
            for i, flag in enumerate(unified_score.red_flags, 1):
                report.append(f"  ⚠ {flag}")
            report.append("")
        
        # Missing Rounds
        if unified_score.missing_rounds:
            report.append("MISSING EVALUATIONS")
            report.append("-" * 70)
            report.append(f"  {', '.join(unified_score.missing_rounds)}")
            report.append("")
        
        # Calculation Notes
        if unified_score.calculation_notes:
            report.append("CALCULATION NOTES")
            report.append("-" * 70)
            for note in unified_score.calculation_notes[-5:]:  # Last 5 notes
                report.append(f"  • {note}")
            report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_summary_report(
        unified_scores: List[UnifiedCandidateScore],
    ) -> str:
        """Generate a summary report for multiple candidates."""
        report = []
        report.append("=" * 70)
        report.append("CANDIDATE HIRING FIT SUMMARY")
        report.append("=" * 70)
        report.append("")
        
        # Sort by fit score
        sorted_scores = sorted(
            unified_scores,
            key=lambda x: x.hiring_fit_percentage,
            reverse=True,
        )
        
        # Table header
        report.append(
            f"{'Rank':<5} {'Candidate':<15} {'Role':<20} {'Fit %':<8} {'Status':<15}"
        )
        report.append("-" * 70)
        
        # Table rows
        for rank, score in enumerate(sorted_scores, 1):
            report.append(
                f"{rank:<5} {score.candidate_id:<15} {score.role:<20} "
                f"{score.hiring_fit_percentage:<8.1f} {score.status.value:<15}"
            )
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)