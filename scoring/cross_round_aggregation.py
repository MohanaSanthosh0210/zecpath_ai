"""Cross-Round Aggregation Engine - Unified hiring intelligence scorer."""

import json
import os
from typing import Dict, Optional, Any, List, Tuple
from pathlib import Path

from schemas.unified_candidate_score import (
    UnifiedCandidateScore,
    RoundScore,
    ScoreWeights,
    HiringFitStatus,
    NormalizationDetails,
)
from scoring.score_normalizer import (
    ScoreNormalizer,
    CandidateProfileNormalizer,
    OutlierDetector,
    RoleBasedNormalizer,
)


class CrossRoundAggregationEngine:
    """
    Aggregate all evaluation stages into a unified hiring intelligence score.
    
    Stages included:
    - ATS (resume screening)
    - Screening (initial phone screen)
    - HR Interview (cultural fit, soft skills)
    - Technical Interview (problem-solving, technical depth)
    - Machine Test (coding ability, execution)
    - Behavioral Intelligence (personality, stress, confidence)
    """
    
    CONFIG_DIR = Path(__file__).parent / "config"
    WEIGHTS_FILE = CONFIG_DIR / "cross_round_weights.json"
    
    # Hiring fit thresholds
    FIT_THRESHOLDS = {
        HiringFitStatus.STRONG_FIT: 85.0,
        HiringFitStatus.GOOD_FIT: 70.0,
        HiringFitStatus.REQUIRES_REVIEW: 55.0,
        HiringFitStatus.CONDITIONAL_FIT: 40.0,
        HiringFitStatus.NOT_FIT: 0.0,
    }
    
    def __init__(self, custom_weights: Optional[Dict[str, Dict[str, float]]] = None):
        """
        Initialize the aggregation engine.
        
        Args:
            custom_weights: Optional custom weights configuration
        """
        self.weights_config = custom_weights or self._load_weights()
    
    @staticmethod
    def _load_weights() -> Dict[str, Dict[str, float]]:
        """Load weights configuration from file."""
        if not CrossRoundAggregationEngine.WEIGHTS_FILE.exists():
            return CrossRoundAggregationEngine._get_default_weights()
        
        with open(CrossRoundAggregationEngine.WEIGHTS_FILE, "r") as f:
            return json.load(f)
    
    @staticmethod
    def _get_default_weights() -> Dict[str, Dict[str, float]]:
        """Get default weights if config file not found."""
        return {
            "default": {
                "ats": 0.20,
                "screening": 0.20,
                "hr_interview": 0.25,
                "technical_interview": 0.25,
                "machine_test": 0.10,
                "behavioral_intelligence": 0.00,
            }
        }
    
    def get_weights_for_role(self, role: str) -> Dict[str, float]:
        """Get weights for a specific role."""
        role_key = role.lower().replace(" ", "_")
        return self.weights_config.get(
            role_key,
            self.weights_config.get("default", self._get_default_weights()["default"])
        )
    
    def validate_weights(self, weights: Dict[str, float]) -> Tuple[bool, str]:
        """Validate that weights sum to 1.0."""
        total = sum(weights.values())
        tolerance = 0.001
        
        if abs(total - 1.0) < tolerance:
            return True, "Weights valid"
        
        return False, f"Weights sum to {total:.3f}, expected 1.0"
    
    def aggregate(
        self,
        candidate_id: str,
        role: str,
        scores: Dict[str, Optional[float]],
        job_id: Optional[str] = None,
        normalize: bool = True,
        detect_outliers: bool = True,
    ) -> UnifiedCandidateScore:
        """
        Aggregate scores from all evaluation stages.
        
        Args:
            candidate_id: Unique candidate identifier
            role: Job role/position
            scores: Dict of round_name -> score (0-100, or None if missing)
            job_id: Optional job/position identifier
            normalize: Whether to normalize scores
            detect_outliers: Whether to detect and handle outliers
            
        Returns:
            UnifiedCandidateScore object with complete scoring breakdown
        """
        unified_score = UnifiedCandidateScore(
            candidate_id=candidate_id,
            job_id=job_id,
            role=role,
        )
        
        # Get role-specific weights
        weights_dict = self.get_weights_for_role(role)
        weights_valid, weight_msg = self.validate_weights(weights_dict)
        
        if not weights_valid:
            unified_score.add_calculation_note(f"Warning: {weight_msg}")
        
        # Set up weights object
        unified_score.weights = ScoreWeights(**weights_dict)
        unified_score.add_calculation_note(f"Applied weights for role: {role}")
        
        # Track valid scores and components
        valid_scores = {}
        outliers_detected = []

        expected_rounds = [
            round_name for round_name in [
                "ats",
                "screening",
                "hr_interview",
                "technical_interview",
                "machine_test",
            ]
            if weights_dict.get(round_name, 0.0) > 0
        ]

        for round_name in expected_rounds:
            if round_name not in scores or scores.get(round_name) is None:
                unified_score.missing_rounds.append(round_name)
        
        # Process each round
        for round_name, score in scores.items():
            if score is None:
                continue
            if round_name not in expected_rounds:
                continue
            
            # Normalize if needed
            normalized_score = score
            if normalize:
                normalized_score, norm_details = self._normalize_score(
                    score, round_name, role
                )
                unified_score.add_calculation_note(
                    f"{round_name}: normalized {score} → {normalized_score}"
                )
            
            # Detect outliers
            if detect_outliers and normalized_score not in [0, 100]:
                is_outlier, outlier_info = self._check_outlier(
                    normalized_score, round_name
                )
                if is_outlier:
                    outliers_detected.append((round_name, outlier_info))
            
            # Create round score
            weight = weights_dict.get(round_name, 0.0)
            weighted_contribution = (normalized_score / 100.0) * weight
            
            round_score = RoundScore(
                round_name=round_name,
                score=score,
                normalized_score=normalized_score,
                weight=weight,
                weighted_contribution=weighted_contribution,
            )
            
            unified_score.add_round_score(round_score)
            valid_scores[round_name] = normalized_score
        
        # Update normalization details
        if outliers_detected:
            unified_score.normalization_details.outliers_detected = True
            unified_score.add_calculation_note(
                f"Outliers detected in: {[x[0] for x in outliers_detected]}"
            )
        
        # Calculate unified score
        unified_score = self._calculate_unified_score(unified_score, valid_scores)
        
        # Determine hiring fit status
        unified_score.status = self._determine_status(unified_score.hiring_fit_percentage)
        
        # Generate insights
        self._generate_insights(unified_score)
        
        return unified_score
    
    def _normalize_score(
        self,
        score: float,
        round_name: str,
        role: str,
    ) -> Tuple[float, Optional[Dict[str, Any]]]:
        """Normalize a score using appropriate method."""
        # Most scores are already 0-100, so minmax with same range
        normalized = ScoreNormalizer.minmax_normalize(score, 0, 100, 0, 100)
        
        # Apply role-specific benchmarks
        benchmarks = RoleBasedNormalizer.ROLE_BENCHMARKS.get(role.lower().replace(" ", "_"))
        if benchmarks and round_name in benchmarks:
            benchmark = benchmarks[round_name]
            # Map to percentile within role's distribution
            normalized = ScoreNormalizer.zscore_normalize(
                score,
                mean=benchmark["mean"],
                std_dev=benchmark["std"],
                target_mean=score,  # Keep original as reference
                target_std=10,
            )
        
        return min(100.0, max(0.0, normalized)), None
    
    def _check_outlier(self, score: float, round_name: str) -> Tuple[bool, Dict[str, Any]]:
        """Check if a score is an outlier for its round type."""
        # Known ranges for different rounds
        normal_ranges = {
            "ats": (30, 95),
            "screening": (20, 100),
            "hr_interview": (40, 100),
            "technical_interview": (10, 95),
            "machine_test": (5, 100),
            "behavioral_intelligence": (20, 95),
        }
        
        if round_name not in normal_ranges:
            return False, {}
        
        min_val, max_val = normal_ranges[round_name]
        is_outlier = score < min_val or score > max_val
        
        return is_outlier, {
            "round": round_name,
            "score": score,
            "normal_range": (min_val, max_val),
        }
    
    def _calculate_unified_score(
        self,
        unified_score: UnifiedCandidateScore,
        valid_scores: Dict[str, float],
    ) -> UnifiedCandidateScore:
        """Calculate the final unified score."""
        if not valid_scores:
            unified_score.unified_score = 0.0
            unified_score.hiring_fit_percentage = 0.0
            unified_score.add_calculation_note("No valid scores to aggregate")
            return unified_score
        
        # Calculate weighted average
        weighted_sum = 0.0
        weight_sum = 0.0
        component_contributions = {}
        
        for round_name, score in valid_scores.items():
            weight = unified_score.weights.to_dict().get(round_name, 0.0)
            contribution = (score / 100.0) * weight
            weighted_sum += contribution
            weight_sum += weight

        # Normalize by actual weight sum (in case some rounds are missing)
        if weight_sum > 0:
            unified_score.unified_score = (weighted_sum / weight_sum) * 100
        else:
            unified_score.unified_score = 0.0

        # Report contribution shares in a transparent, role-weighted way.
        for round_name, score in valid_scores.items():
            weight = unified_score.weights.to_dict().get(round_name, 0.0)
            if weight_sum > 0:
                component_contributions[round_name] = round((weight / weight_sum) * 100, 2)
            else:
                component_contributions[round_name] = 0.0
        
        unified_score.hiring_fit_percentage = round(
            unified_score.unified_score, 2
        )
        unified_score.component_contributions = component_contributions
        
        return unified_score
    
    def _determine_status(self, fit_percentage: float) -> HiringFitStatus:
        """Determine hiring fit status based on percentage."""
        for status, threshold in sorted(
            self.FIT_THRESHOLDS.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            if fit_percentage >= threshold:
                return status
        
        return HiringFitStatus.NOT_FIT
    
    def _generate_insights(self, unified_score: UnifiedCandidateScore) -> None:
        """Generate insights and recommendations."""
        scores = unified_score.round_scores
        fit = unified_score.hiring_fit_percentage
        
        # Identify strengths
        strong_rounds = [
            name for name, score in scores.items()
            if score.normalized_score >= 80
        ]
        for round_name in strong_rounds:
            unified_score.add_strength(
                f"Strong performance in {round_name}: {scores[round_name].normalized_score}"
            )
        
        # Identify weaknesses
        weak_rounds = [
            name for name, score in scores.items()
            if score.normalized_score < 50
        ]
        for round_name in weak_rounds:
            unified_score.add_concern(
                f"Weak performance in {round_name}: {scores[round_name].normalized_score}"
            )
        
        # Generate recommendation
        if unified_score.status == HiringFitStatus.STRONG_FIT:
            unified_score.recommendation = "Recommend for hire - Strong fit"
            unified_score.decision = "APPROVE"
        elif unified_score.status == HiringFitStatus.GOOD_FIT:
            unified_score.recommendation = "Recommend for hire - Good fit"
            unified_score.decision = "APPROVE"
        elif unified_score.status == HiringFitStatus.REQUIRES_REVIEW:
            unified_score.recommendation = "Needs detailed review - Moderate fit"
            unified_score.decision = "REVIEW"
        elif unified_score.status == HiringFitStatus.CONDITIONAL_FIT:
            unified_score.recommendation = "Consider for junior roles or with training"
            unified_score.decision = "CONDITIONAL"
        else:
            unified_score.recommendation = "Not recommended for this role"
            unified_score.decision = "REJECT"
        
        # Red flags
        if unified_score.missing_rounds and len(unified_score.missing_rounds) > 2:
            unified_score.add_red_flag("Multiple evaluation stages missing")
        
        if len(weak_rounds) > 2:
            unified_score.add_red_flag("Weakness in multiple evaluation stages")


class HiringFitCalculator:
    """Simplified hiring fit calculator for quick assessments."""
    
    def __init__(self):
        self.engine = CrossRoundAggregationEngine()
    
    def calculate(
        self,
        candidate_id: str,
        role: str,
        **round_scores,
    ) -> Dict[str, Any]:
        """
        Quick calculation of hiring fit.
        
        Args:
            candidate_id: Candidate ID
            role: Job role
            **round_scores: Keyword arguments for each round
                (ats_score=X, screening_score=Y, etc.)
                
        Returns:
            Dictionary with hiring fit results
        """
        # Convert keyword args to the expected format
        scores_dict = {}
        for key, value in round_scores.items():
            # Convert "ats_score" -> "ats", etc.
            if key.endswith("_score"):
                round_name = key[:-6]  # Remove "_score"
            else:
                round_name = key
            scores_dict[round_name] = value
        
        unified_score = self.engine.aggregate(
            candidate_id=candidate_id,
            role=role,
            scores=scores_dict,
        )
        
        return unified_score.to_dict()
    
    def calculate_batch(
        self,
        candidates: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Calculate hiring fit for multiple candidates.
        
        Args:
            candidates: List of candidate dicts with candidate_id, role, and scores
            
        Returns:
            List of hiring fit results
        """
        results = []
        for candidate in candidates:
            candidate_id = candidate.get("candidate_id", "")
            role = candidate.get("role", "")
            scores = {k: v for k, v in candidate.items()
                     if k not in ["candidate_id", "role", "job_id"]}
            
            result = self.calculate(
                candidate_id=candidate_id,
                role=role,
                **scores
            )
            results.append(result)
        
        return results