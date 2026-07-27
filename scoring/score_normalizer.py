"""Score normalization utilities for cross-round aggregation."""

from typing import Dict, List, Tuple, Optional, Any
import math
import statistics


class ScoreNormalizer:
    """Normalize scores across different evaluation stages and profiles."""
    
    STANDARD_SCALE = (0.0, 100.0)
    
    @staticmethod
    def minmax_normalize(
        value: float,
        value_min: float = 0.0,
        value_max: float = 100.0,
        target_min: float = 0.0,
        target_max: float = 100.0,
    ) -> float:
        """
        Normalize using min-max scaling.
        
        Formula: (value - min) / (max - min) * (target_max - target_min) + target_min
        """
        if value_max == value_min:
            return target_min
        
        normalized = (value - value_min) / (value_max - value_min)
        return normalized * (target_max - target_min) + target_min
    
    @staticmethod
    def zscore_normalize(
        value: float,
        mean: float,
        std_dev: float,
        target_mean: float = 50.0,
        target_std: float = 15.0,
    ) -> float:
        """
        Normalize using z-score transformation.
        
        Formula: ((value - mean) / std_dev) * target_std + target_mean
        """
        if std_dev == 0:
            return target_mean
        
        z_score = (value - mean) / std_dev
        return z_score * target_std + target_mean
    
    @staticmethod
    def percentile_normalize(
        value: float,
        distribution: List[float],
    ) -> float:
        """
        Normalize based on percentile rank in a distribution.
        Returns percentile (0-100).
        """
        if not distribution:
            return 50.0
        
        sorted_dist = sorted(distribution)
        if value <= sorted_dist[0]:
            return 0.0
        if value >= sorted_dist[-1]:
            return 100.0

        count_below = sum(1 for x in sorted_dist if x < value)
        count_equal = sum(1 for x in sorted_dist if x == value)
        rank = count_below + (0.5 * count_equal)
        percentile = (rank / len(sorted_dist)) * 100
        return max(0.0, min(100.0, percentile))
    
    @staticmethod
    def sigmoid_normalize(
        value: float,
        inflection_point: float = 50.0,
        steepness: float = 0.1,
    ) -> float:
        """
        Normalize using sigmoid function for smooth scaling.
        Useful for mapping scores to probability-like values.
        """
        try:
            sigmoid = 1 / (1 + math.exp(-steepness * (value - inflection_point)))
            return sigmoid * 100
        except (OverflowError, ValueError):
            return 50.0
    
    @staticmethod
    def robust_normalize(
        value: float,
        q1: float,
        q3: float,
        median: float,
        target_min: float = 0.0,
        target_max: float = 100.0,
    ) -> float:
        """
        Robust normalization using quartiles (resistant to outliers).
        """
        iqr = q3 - q1
        
        if iqr == 0:
            return (target_min + target_max) / 2
        
        # Normalize relative to quartiles
        normalized = (value - median) / (1.35 * iqr)
        # Clip to reasonable range
        normalized = max(-3, min(3, normalized))
        # Map to target range
        return ((normalized + 3) / 6) * (target_max - target_min) + target_min
    
    @staticmethod
    def linear_interpolation(
        value: float,
        reference_points: List[Tuple[float, float]],
    ) -> float:
        """
        Linear interpolation based on reference points.
        reference_points: List of (input, output) tuples
        """
        if not reference_points:
            return value
        
        sorted_points = sorted(reference_points, key=lambda x: x[0])
        
        # Find the two points to interpolate between
        for i in range(len(sorted_points) - 1):
            x1, y1 = sorted_points[i]
            x2, y2 = sorted_points[i + 1]
            
            if x1 <= value <= x2:
                if x2 == x1:
                    return y1
                slope = (y2 - y1) / (x2 - x1)
                return y1 + slope * (value - x1)
        
        # If value is outside range, return closest point
        if value < sorted_points[0][0]:
            return sorted_points[0][1]
        return sorted_points[-1][1]


class CandidateProfileNormalizer:
    """Normalize scores across different candidate profiles."""
    
    @staticmethod
    def normalize_by_experience_level(
        score: float,
        experience_years: float,
        role: str,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Adjust scores based on candidate experience level.
        Junior candidates may have lower technical scores but high potential.
        """
        adjustment_factor = 1.0
        notes = []
        
        if experience_years < 1:
            # Fresher - adjust expectations
            adjustment_factor = 0.95
            notes.append("Adjustment: Fresher profile - expectations calibrated")
        elif experience_years < 3:
            # Junior
            adjustment_factor = 0.98
            notes.append("Adjustment: Junior profile - minor calibration")
        elif experience_years < 5:
            # Mid-level
            adjustment_factor = 1.0
            notes.append("No adjustment: Mid-level profile - baseline expectations")
        elif experience_years < 10:
            # Senior
            adjustment_factor = 1.02
            notes.append("Adjustment: Senior profile - higher expectations")
        else:
            # Principal/Lead
            adjustment_factor = 1.05
            notes.append("Adjustment: Principal profile - expert expectations")
        
        adjusted_score = score * adjustment_factor
        adjusted_score = min(100.0, max(0.0, adjusted_score))
        
        return adjusted_score, {
            "original_score": score,
            "adjusted_score": adjusted_score,
            "experience_years": experience_years,
            "adjustment_factor": adjustment_factor,
            "notes": notes,
        }
    
    @staticmethod
    def normalize_by_background(
        score: float,
        background_type: str,  # "traditional", "bootcamp", "self-taught", "career_switch"
        role: str,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Adjust scores based on candidate background/education type.
        """
        adjustment_factors = {
            "traditional": 1.0,
            "bootcamp": 0.98,
            "self_taught": 0.95,
            "career_switch": 0.92,
        }
        
        adjustment_factor = adjustment_factors.get(background_type, 1.0)
        adjusted_score = score * adjustment_factor
        adjusted_score = min(100.0, max(0.0, adjusted_score))
        
        return adjusted_score, {
            "original_score": score,
            "adjusted_score": adjusted_score,
            "background_type": background_type,
            "adjustment_factor": adjustment_factor,
            "notes": [f"Background adjustment: {background_type}"],
        }
    
    @staticmethod
    def normalize_by_location_market(
        score: float,
        location: str,
        cost_of_living_index: float,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Adjust expectations based on location and cost of living.
        Candidates from high CoL areas may have access to better resources.
        """
        # Normalize cost of living index (assume 100 = baseline)
        adjustment_factor = 1.0 + (cost_of_living_index - 100) / 1000
        adjustment_factor = max(0.95, min(1.05, adjustment_factor))
        
        adjusted_score = score * adjustment_factor
        adjusted_score = min(100.0, max(0.0, adjusted_score))
        
        return adjusted_score, {
            "original_score": score,
            "adjusted_score": adjusted_score,
            "location": location,
            "cost_of_living_index": cost_of_living_index,
            "adjustment_factor": adjustment_factor,
            "notes": [f"Location adjustment: {location}"],
        }


class OutlierDetector:
    """Detect and handle outliers in score distributions."""
    
    @staticmethod
    def detect_iqr(
        values: List[float],
        multiplier: float = 1.5,
    ) -> Tuple[List[int], Dict[str, Any]]:
        """
        Detect outliers using Interquartile Range (IQR) method.
        Returns indices of outliers.
        """
        if len(values) < 4:
            return [], {"method": "iqr", "outlier_indices": []}
        
        sorted_values = sorted(values)
        q1_idx = len(sorted_values) // 4
        q3_idx = (3 * len(sorted_values)) // 4
        
        q1 = sorted_values[q1_idx]
        q3 = sorted_values[q3_idx]
        iqr = q3 - q1
        
        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr
        
        outlier_indices = [
            i for i, v in enumerate(values)
            if v < lower_bound or v > upper_bound
        ]
        
        return outlier_indices, {
            "method": "iqr",
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_indices": outlier_indices,
        }
    
    @staticmethod
    def detect_zscore(
        values: List[float],
        threshold: float = 2.0,
    ) -> Tuple[List[int], Dict[str, Any]]:
        """
        Detect outliers using z-score method.
        Returns indices of outliers.
        """
        if len(values) < 2:
            return [], {"method": "zscore", "outlier_indices": []}
        
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0
        
        if stdev == 0:
            return [], {"method": "zscore", "outlier_indices": []}
        
        outlier_indices = [
            i for i, v in enumerate(values)
            if abs((v - mean) / stdev) > threshold
        ]
        
        return outlier_indices, {
            "method": "zscore",
            "mean": mean,
            "stdev": stdev,
            "threshold": threshold,
            "outlier_indices": outlier_indices,
        }
    
    @staticmethod
    def handle_outliers(
        value: float,
        values: List[float],
        method: str = "cap",
    ) -> Tuple[float, float]:
        """
        Handle outlier values.
        
        Methods:
        - "cap": Cap to percentile (e.g., 95th percentile)
        - "winsorize": Winsorize at percentile
        - "keep": Keep as is
        """
        if not values or len(values) < 2:
            return value, 0.0
        
        sorted_values = sorted(values)
        p95 = sorted_values[int(0.95 * len(sorted_values))]
        p5 = sorted_values[int(0.05 * len(sorted_values))]
        
        adjustment = 0.0
        
        if method == "cap":
            if value > p95:
                adjustment = value - p95
                value = p95
            elif value < p5:
                adjustment = p5 - value
                value = p5
        elif method == "winsorize":
            if value > p95:
                adjustment = value - p95
                value = p95
            elif value < p5:
                adjustment = value - p5
                value = p5
        
        return value, adjustment


class RoleBasedNormalizer:
    """Apply role-specific normalization rules."""
    
    ROLE_BENCHMARKS = {
        "python_developer": {
            "technical_interview": {"mean": 72, "std": 12},
            "machine_test": {"mean": 68, "std": 15},
        },
        "data_scientist": {
            "technical_interview": {"mean": 70, "std": 14},
            "machine_test": {"mean": 65, "std": 18},
        },
        "frontend_developer": {
            "technical_interview": {"mean": 68, "std": 13},
            "machine_test": {"mean": 65, "std": 16},
        },
    }
    
    @staticmethod
    def normalize_for_role(
        scores: Dict[str, float],
        role: str,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Normalize scores based on role-specific benchmarks.
        """
        result = {}
        benchmarks = RoleBasedNormalizer.ROLE_BENCHMARKS.get(role, {})
        
        for round_name, score in scores.items():
            if round_name in benchmarks:
                benchmark = benchmarks[round_name]
                normalized_score = ScoreNormalizer.zscore_normalize(
                    score,
                    mean=benchmark["mean"],
                    std_dev=benchmark["std"],
                )
                result[round_name] = {
                    "original_score": score,
                    "normalized_score": normalized_score,
                    "benchmark_mean": benchmark["mean"],
                    "benchmark_std": benchmark["std"],
                }
            else:
                result[round_name] = {
                    "original_score": score,
                    "normalized_score": score,
                    "benchmark_mean": None,
                    "benchmark_std": None,
                }
        
        return result