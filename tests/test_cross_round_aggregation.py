"""Unit tests for Cross-Round Aggregation Engine."""

import pytest
import math
from schemas.unified_candidate_score import (
    UnifiedCandidateScore,
    RoundScore,
    ScoreWeights,
    HiringFitStatus,
)
from scoring.cross_round_aggregation import (
    CrossRoundAggregationEngine,
    HiringFitCalculator,
)
from scoring.score_normalizer import (
    ScoreNormalizer,
    CandidateProfileNormalizer,
    OutlierDetector,
)
from scoring.aggregation_pipeline import CrossRoundScoringPipeline


class TestScoreNormalizer:
    """Test score normalization methods."""
    
    def test_minmax_normalize(self):
        """Test min-max scaling."""
        # Normalize 50 from 0-100 to 0-100
        result = ScoreNormalizer.minmax_normalize(50, 0, 100, 0, 100)
        assert result == 50
        
        # Normalize 75 from 0-100 to 0-10
        result = ScoreNormalizer.minmax_normalize(75, 0, 100, 0, 10)
        assert abs(result - 7.5) < 0.01
        
        # Edge case: same min and max
        result = ScoreNormalizer.minmax_normalize(50, 50, 50, 0, 100)
        assert result == 0
    
    def test_zscore_normalize(self):
        """Test z-score normalization."""
        # Score at mean should give mean target
        result = ScoreNormalizer.zscore_normalize(70, mean=70, std_dev=10)
        assert abs(result - 50) < 0.01  # Default target mean is 50
        
        # Zero std dev
        result = ScoreNormalizer.zscore_normalize(70, mean=70, std_dev=0)
        assert result == 50
    
    def test_percentile_normalize(self):
        """Test percentile normalization."""
        distribution = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        
        # Value at start
        result = ScoreNormalizer.percentile_normalize(10, distribution)
        assert result < 10
        
        # Value at end
        result = ScoreNormalizer.percentile_normalize(100, distribution)
        assert result > 90
        
        # Empty distribution
        result = ScoreNormalizer.percentile_normalize(50, [])
        assert result == 50.0
    
    def test_sigmoid_normalize(self):
        """Test sigmoid normalization."""
        # At inflection point, should be ~50
        result = ScoreNormalizer.sigmoid_normalize(50, inflection_point=50)
        assert 45 < result < 55
        
        # Very high value, should be ~100
        result = ScoreNormalizer.sigmoid_normalize(100, inflection_point=50, steepness=0.1)
        assert result > 90
        
        # Very low value, should be ~0
        result = ScoreNormalizer.sigmoid_normalize(0, inflection_point=50, steepness=0.1)
        assert result < 10


class TestCandidateProfileNormalizer:
    """Test profile-based normalization."""
    
    def test_normalize_by_experience_level(self):
        """Test experience-based adjustment."""
        # Fresher (< 1 year)
        score, details = CandidateProfileNormalizer.normalize_by_experience_level(
            80, 0.5, "python_developer"
        )
        assert score <= 80  # Should be adjusted down
        assert details["adjustment_factor"] == 0.95
        
        # Senior (5-10 years)
        score, details = CandidateProfileNormalizer.normalize_by_experience_level(
            80, 7, "python_developer"
        )
        assert score >= 80  # Should be adjusted up
        assert details["adjustment_factor"] == 1.02
    
    def test_normalize_by_background(self):
        """Test background-based adjustment."""
        # Traditional (no adjustment)
        score, details = CandidateProfileNormalizer.normalize_by_experience_level(
            80, 5, "python_developer"
        )
        original = score
        
        # Career switch (downward adjustment)
        score, details = CandidateProfileNormalizer.normalize_by_background(
            80, "career_switch", "python_developer"
        )
        assert score < 80


class TestOutlierDetector:
    """Test outlier detection."""
    
    def test_detect_iqr(self):
        """Test IQR-based outlier detection."""
        values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 200]  # 200 is outlier
        
        outlier_indices, info = OutlierDetector.detect_iqr(values)
        assert len(outlier_indices) > 0
        assert 9 in outlier_indices  # 200 is at index 9
    
    def test_detect_zscore(self):
        """Test z-score outlier detection."""
        values = [50, 51, 52, 53, 54, 55, 56, 57, 58, 200]  # 200 is outlier
        
        outlier_indices, info = OutlierDetector.detect_zscore(values, threshold=2.0)
        assert len(outlier_indices) > 0
        assert 9 in outlier_indices


class TestCrossRoundAggregationEngine:
    """Test the main aggregation engine."""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        return CrossRoundAggregationEngine()
    
    def test_validate_weights(self, engine):
        """Test weight validation."""
        valid_weights = {"a": 0.3, "b": 0.3, "c": 0.4}
        is_valid, msg = engine.validate_weights(valid_weights)
        assert is_valid
        
        invalid_weights = {"a": 0.5, "b": 0.3}
        is_valid, msg = engine.validate_weights(invalid_weights)
        assert not is_valid
    
    def test_get_weights_for_role(self, engine):
        """Test retrieving role-specific weights."""
        weights = engine.get_weights_for_role("python_developer")
        assert weights is not None
        assert "ats" in weights
        
        # Sum should be approximately 1.0
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.01
    
    def test_aggregate_all_scores(self, engine):
        """Test aggregation with all scores."""
        result = engine.aggregate(
            candidate_id="TEST-001",
            role="python_developer",
            scores={
                "ats": 80,
                "screening": 75,
                "hr_interview": 85,
                "technical_interview": 90,
                "machine_test": 88,
            }
        )
        
        assert result.candidate_id == "TEST-001"
        assert result.role == "python_developer"
        assert result.hiring_fit_percentage > 0
        assert result.hiring_fit_percentage <= 100
        assert len(result.round_scores) == 5
    
    def test_aggregate_partial_scores(self, engine):
        """Test aggregation with missing scores."""
        result = engine.aggregate(
            candidate_id="TEST-002",
            role="python_developer",
            scores={
                "ats": 80,
                "screening": 75,
                "technical_interview": 90,
            }
        )
        
        assert result.candidate_id == "TEST-002"
        assert len(result.round_scores) == 3
        assert "hr_interview" in result.missing_rounds
        assert "machine_test" in result.missing_rounds
    
    def test_status_determination(self, engine):
        """Test hiring fit status determination."""
        # Strong fit
        result = engine.aggregate(
            candidate_id="STRONG",
            role="python_developer",
            scores={"ats": 90, "screening": 92, "hr_interview": 88}
        )
        assert result.status == HiringFitStatus.STRONG_FIT
        
        # Good fit
        result = engine.aggregate(
            candidate_id="GOOD",
            role="python_developer",
            scores={"ats": 75, "screening": 75, "hr_interview": 75}
        )
        assert result.status == HiringFitStatus.GOOD_FIT
        
        # Not fit
        result = engine.aggregate(
            candidate_id="BAD",
            role="python_developer",
            scores={"ats": 35, "screening": 40, "hr_interview": 38}
        )
        assert result.status == HiringFitStatus.NOT_FIT
    
    def test_component_contributions(self, engine):
        """Test component contribution calculation."""
        result = engine.aggregate(
            candidate_id="TEST-003",
            role="python_developer",
            scores={
                "ats": 80,
                "screening": 80,
                "hr_interview": 80,
                "technical_interview": 80,
                "machine_test": 80,
            }
        )
        
        # All scores equal, contributions should be proportional to weights
        total_contribution = sum(result.component_contributions.values())
        assert abs(total_contribution - 100) < 1  # Should sum to ~100
    
    def test_missing_rounds_tracking(self, engine):
        """Test tracking of missing evaluation rounds."""
        result = engine.aggregate(
            candidate_id="TEST-004",
            role="python_developer",
            scores={"ats": 80, "screening": 75}
        )
        
        assert "hr_interview" in result.missing_rounds
        assert "technical_interview" in result.missing_rounds
        assert len(result.missing_rounds) > 0


class TestUnifiedCandidateScore:
    """Test unified score schema."""
    
    def test_score_creation(self):
        """Test creating a unified score object."""
        score = UnifiedCandidateScore(
            candidate_id="TEST-001",
            role="python_developer",
        )
        
        assert score.candidate_id == "TEST-001"
        assert score.role == "python_developer"
        assert len(score.round_scores) == 0
    
    def test_add_round_score(self):
        """Test adding round scores."""
        score = UnifiedCandidateScore(candidate_id="TEST", role="test")
        
        round_score = RoundScore(
            round_name="ats",
            score=80,
            normalized_score=80,
            weight=0.2,
        )
        
        score.add_round_score(round_score)
        assert "ats" in score.round_scores
        assert score.round_scores["ats"].score == 80
    
    def test_to_dict_conversion(self):
        """Test converting to dictionary."""
        score = UnifiedCandidateScore(
            candidate_id="TEST-001",
            role="python_developer",
        )
        score.unified_score = 82.5
        score.hiring_fit_percentage = 82.5
        
        data = score.to_dict()
        assert data["candidate_id"] == "TEST-001"
        assert data["unified_score"] == 82.5
        assert data["hiring_fit_percentage"] == 82.5
    
    def test_insights_generation(self):
        """Test insight generation."""
        score = UnifiedCandidateScore(
            candidate_id="TEST",
            role="test",
        )
        
        score.add_strength("Excellent communication skills")
        score.add_concern("Limited experience")
        score.add_red_flag("Missing key evaluation")
        
        assert len(score.strengths) == 1
        assert len(score.concerns) == 1
        assert len(score.red_flags) == 1


class TestHiringFitCalculator:
    """Test quick hiring fit calculator."""
    
    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return HiringFitCalculator()
    
    def test_single_calculation(self, calculator):
        """Test single candidate calculation."""
        result = calculator.calculate(
            candidate_id="TEST-001",
            role="python_developer",
            ats_score=80,
            screening_score=75,
            hr_interview_score=85,
            technical_interview_score=90,
        )
        
        assert result["candidate_id"] == "TEST-001"
        assert result["hiring_fit_percentage"] > 0
        assert "status" in result
    
    def test_batch_calculation(self, calculator):
        """Test batch calculation."""
        candidates = [
            {"candidate_id": "C1", "role": "python_developer", "ats": 80, "screening": 75},
            {"candidate_id": "C2", "role": "python_developer", "ats": 70, "screening": 65},
        ]
        
        results = calculator.calculate_batch(candidates)
        assert len(results) == 2
        assert results[0]["candidate_id"] == "C1"
        assert results[1]["candidate_id"] == "C2"


class TestCrossRoundScoringPipeline:
    """Test the complete pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline instance."""
        return CrossRoundScoringPipeline()
    
    def test_process_single_candidate(self, pipeline):
        """Test processing a single candidate."""
        result = pipeline.process_candidate(
            candidate_id="PIPE-001",
            role="python_developer",
            ats_score=80,
            screening_score=75,
            hr_interview_score=85,
        )
        
        assert isinstance(result, UnifiedCandidateScore)
        assert result.candidate_id == "PIPE-001"
    
    def test_process_batch(self, pipeline):
        """Test batch processing."""
        candidates = [
            {"candidate_id": "B1", "role": "python_developer", "ats": 85, "screening": 80},
            {"candidate_id": "B2", "role": "python_developer", "ats": 70, "screening": 75},
        ]
        
        results = pipeline.process_batch(candidates)
        assert len(results) == 2
        assert len(pipeline.results) == 2
    
    def test_comparison_report(self, pipeline):
        """Test generating comparison report."""
        candidates = [
            {"candidate_id": "C1", "role": "python_developer", "ats": 85, "screening": 80},
            {"candidate_id": "C2", "role": "python_developer", "ats": 70, "screening": 75},
        ]
        
        pipeline.process_batch(candidates)
        report = pipeline.generate_comparison_report()
        
        assert report["total_candidates"] == 2
        assert "statistics" in report
        assert "recommendations" in report
        assert len(report["candidates"]) == 2
    
    def test_clear_results(self, pipeline):
        """Test clearing results."""
        pipeline.results.append(UnifiedCandidateScore(candidate_id="TEST", role="test"))
        assert len(pipeline.results) == 1
        
        pipeline.clear_results()
        assert len(pipeline.results) == 0


class TestIntegration:
    """Integration tests."""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from raw scores to report."""
        pipeline = CrossRoundScoringPipeline()
        
        candidates = [
            {
                "candidate_id": "INT-001",
                "role": "python_developer",
                "ats": 85, "screening": 82,
                "hr_interview": 88, "technical_interview": 92,
                "machine_test": 89,
            },
            {
                "candidate_id": "INT-002",
                "role": "python_developer",
                "ats": 65, "screening": 68,
                "hr_interview": 70, "technical_interview": 72,
            },
        ]
        
        results = pipeline.process_batch(candidates)
        report = pipeline.generate_comparison_report()
        
        # Verify results
        assert len(results) == 2
        assert results[0].hiring_fit_percentage > results[1].hiring_fit_percentage
        
        # Verify report
        assert report["total_candidates"] == 2
        assert report["candidates"][0]["rank"] == 1  # Higher score should be rank 1
        assert report["statistics"]["average_fit_score"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
