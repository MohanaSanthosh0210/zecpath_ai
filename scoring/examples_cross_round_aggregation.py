"""
Cross-Round Aggregation Engine - Comprehensive Examples
Day 51 Deliverable Demo
"""

from scoring.aggregation_pipeline import (
    CrossRoundScoringPipeline,
    AggregationReportGenerator,
)
from scoring.cross_round_aggregation import (
    CrossRoundAggregationEngine,
    HiringFitCalculator,
)
from schemas.unified_candidate_score import UnifiedCandidateScore
import json
from pathlib import Path


def example_1_single_candidate():
    """Example 1: Calculate hiring fit for a single candidate."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Single Candidate Hiring Fit Calculation")
    print("="*70)
    
    engine = CrossRoundAggregationEngine()
    
    result = engine.aggregate(
        candidate_id="CAND-2024-001",
        role="python_developer",
        scores={
            "ats": 82,
            "screening": 78,
            "hr_interview": 85,
            "technical_interview": 92,
            "machine_test": 88,
        },
    )
    
    print(f"\nCandidate ID: {result.candidate_id}")
    print(f"Role: {result.role}")
    print(f"\nHiring Fit Score: {result.hiring_fit_percentage}%")
    print(f"Status: {result.status.value}")
    print(f"Decision: {result.decision}")
    print(f"Recommendation: {result.recommendation}")
    print(f"\nMissing Rounds: {result.missing_rounds if result.missing_rounds else 'None'}")
    print(f"Red Flags: {result.red_flags if result.red_flags else 'None'}")
    
    print("\nRound Scores:")
    for round_name, score in result.round_scores.items():
        print(f"  {round_name:25s}: {score.normalized_score:6.2f}/100 (weight: {score.weight:.0%})")
    
    print("\nComponent Contributions:")
    for round_name, contribution in result.component_contributions.items():
        bar = "█" * int(contribution / 4)
        print(f"  {round_name:25s}: {contribution:6.2f}% {bar}")
    
    print("\nStrengths:")
    for i, strength in enumerate(result.strengths, 1):
        print(f"  {i}. {strength}")
    
    return result


def example_2_quick_calculation():
    """Example 2: Quick hiring fit calculation using calculator."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Quick Hiring Fit Calculator")
    print("="*70)
    
    calculator = HiringFitCalculator()
    
    result = calculator.calculate(
        candidate_id="CAND-2024-002",
        role="data_scientist",
        ats_score=72,
        screening_score=75,
        hr_interview_score=70,
        technical_interview_score=78,
        machine_test_score=82,
    )
    
    print(f"\nCandidates: {result['candidate_id']}")
    print(f"Hiring Fit: {result['hiring_fit_percentage']}%")
    print(f"Status: {result['status']}")
    print(f"Decision: {result['decision']}")
    print(f"Recommendation: {result['recommendation']}")
    
    return result


def example_3_batch_processing():
    """Example 3: Process multiple candidates and compare."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Batch Processing & Candidate Comparison")
    print("="*70)
    
    pipeline = CrossRoundScoringPipeline()
    
    candidates = [
        {
            "candidate_id": "CAND-2024-A",
            "role": "python_developer",
            "ats": 88, "screening": 85, "hr_interview": 87,
            "technical_interview": 92, "machine_test": 89,
        },
        {
            "candidate_id": "CAND-2024-B",
            "role": "python_developer",
            "ats": 72, "screening": 75, "hr_interview": 68,
            "technical_interview": 78, "machine_test": 85,
        },
        {
            "candidate_id": "CAND-2024-C",
            "role": "python_developer",
            "ats": 65, "screening": 68, "hr_interview": 70,
            "technical_interview": 60, "machine_test": 72,
        },
        {
            "candidate_id": "CAND-2024-D",
            "role": "python_developer",
            "ats": 45, "screening": 50, "hr_interview": 55,
            "technical_interview": 48, "machine_test": 52,
        },
    ]
    
    # Process all candidates
    print("\nProcessing candidates...")
    results = pipeline.process_batch(candidates)
    
    # Print individual summaries
    print("\nIndividual Results:")
    for result in results:
        print(f"  {result.candidate_id}: {result.hiring_fit_percentage}% ({result.status.value})")
    
    # Generate comparison report
    comparison_report = pipeline.generate_comparison_report()
    
    print("\nComparison Report:")
    print(f"Total Candidates: {comparison_report['total_candidates']}")
    
    print("\nRankings:")
    for cand in comparison_report["candidates"][:3]:
        print(f"  #{cand['rank']} - {cand['candidate_id']}: {cand['hiring_fit_percentage']}% ({cand['decision']})")
    
    print("\nStatistics:")
    stats = comparison_report["statistics"]
    print(f"  Average Fit Score: {stats['average_fit_score']}%")
    print(f"  Range: {stats['min_fit_score']}% - {stats['max_fit_score']}%")
    print(f"  Std Deviation: {stats['std_deviation']}%")
    
    print("\nRecommendations:")
    for rec in comparison_report["recommendations"]:
        print(f"  • {rec}")
    
    return results, comparison_report


def example_4_different_roles():
    """Example 4: See how different roles get different weightage."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Role-Specific Weightage System")
    print("="*70)
    
    engine = CrossRoundAggregationEngine()
    
    # Same candidate scores, different roles
    test_scores = {
        "ats": 75,
        "screening": 75,
        "hr_interview": 75,
        "technical_interview": 75,
        "machine_test": 75,
    }
    
    roles = ["python_developer", "product_manager", "data_scientist"]
    
    print("\nSame candidate scores (all 75%) with different role weightage:")
    print("-" * 70)
    
    for role in roles:
        result = engine.aggregate(
            candidate_id="TEST-CANDIDATE",
            role=role,
            scores=test_scores,
        )
        
        weights = engine.get_weights_for_role(role)
        print(f"\n{role.upper()}")
        print(f"  Weights: ATS={weights['ats']:.0%}, Screening={weights['screening']:.0%}, "
              f"HR={weights['hr_interview']:.0%}, Tech={weights['technical_interview']:.0%}, "
              f"Machine={weights['machine_test']:.0%}")
        print(f"  Final Hiring Fit: {result.hiring_fit_percentage}%")


def example_5_missing_scores():
    """Example 5: Handle missing evaluation rounds."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Handling Missing Evaluation Rounds")
    print("="*70)
    
    engine = CrossRoundAggregationEngine()
    
    # Candidate with incomplete evaluations
    incomplete_scores = {
        "ats": 80,
        "screening": 85,
        "hr_interview": None,  # Missing
        "technical_interview": 78,
        # Machine test not done yet
    }
    
    result = engine.aggregate(
        candidate_id="CAND-INCOMPLETE",
        role="python_developer",
        scores=incomplete_scores,
    )
    
    print(f"\nCandidate: {result.candidate_id}")
    print(f"Hiring Fit Score: {result.hiring_fit_percentage}%")
    print(f"\nCompleted Rounds:")
    for round_name, score in result.round_scores.items():
        print(f"  • {round_name}: {score.normalized_score}")
    
    print(f"\nMissing Rounds: {', '.join(result.missing_rounds)}")
    print(f"\nCalculation Notes:")
    for note in result.calculation_notes:
        print(f"  • {note}")


def example_6_detailed_report():
    """Example 6: Generate detailed candidate report."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Detailed Candidate Report")
    print("="*70)
    
    engine = CrossRoundAggregationEngine()
    
    result = engine.aggregate(
        candidate_id="CAND-REPORT-001",
        role="frontend_developer",
        scores={
            "ats": 78,
            "screening": 80,
            "hr_interview": 85,
            "technical_interview": 82,
            "machine_test": 75,
            "behavioral_intelligence": 88,
        },
    )
    
    report = AggregationReportGenerator.generate_candidate_report(result)
    print(report)
    
    return result


def example_7_custom_weights():
    """Example 7: Use custom weights for specialized role."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Custom Weightage for Specialized Role")
    print("="*70)
    
    # Define custom weights for specialized role
    custom_weights = {
        "ml_researcher": {
            "ats": 0.10,
            "screening": 0.10,
            "hr_interview": 0.15,
            "technical_interview": 0.45,  # Heavily weighted
            "machine_test": 0.20,
            "behavioral_intelligence": 0.00,
        }
    }
    
    engine = CrossRoundAggregationEngine(custom_weights=custom_weights)
    
    # Test candidate
    result = engine.aggregate(
        candidate_id="CAND-ML-SPECIALIST",
        role="ml_researcher",
        scores={
            "ats": 70,
            "screening": 72,
            "hr_interview": 75,
            "technical_interview": 95,  # Excellent in technical
            "machine_test": 88,
        },
    )
    
    print(f"\nRole: ML Researcher (Custom Weights)")
    print(f"Hiring Fit Score: {result.hiring_fit_percentage}%")
    
    print("\nWeights Applied:")
    for round_name, weight in result.weights.to_dict().items():
        if weight > 0:
            print(f"  {round_name}: {weight:.0%}")
    
    print("\nComponent Contributions:")
    for round_name, contribution in result.component_contributions.items():
        bar = "█" * int(contribution / 3)
        print(f"  {round_name:25s}: {contribution:5.1f}% {bar}")


def example_8_export_results():
    """Example 8: Export results to JSON and CSV."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Export Results")
    print("="*70)
    
    pipeline = CrossRoundScoringPipeline()
    
    candidates = [
        {
            "candidate_id": "EXPORT-001",
            "role": "python_developer",
            "ats": 85, "screening": 82, "hr_interview": 88,
            "technical_interview": 90, "machine_test": 87,
        },
        {
            "candidate_id": "EXPORT-002",
            "role": "python_developer",
            "ats": 72, "screening": 75, "hr_interview": 70,
            "technical_interview": 76, "machine_test": 78,
        },
    ]
    
    pipeline.process_batch(candidates)
    
    # Export to JSON
    json_file = "scoring_results.json"
    pipeline.export_results(json_file, format="json")
    print(f"\n✓ Exported to {json_file}")
    
    # Show sample of exported data
    with open(json_file, "r") as f:
        data = json.load(f)
    
    print(f"\nExported {len(data)} candidate(s)")
    print(f"Sample: {data[0]['candidate_id']} - {data[0]['hiring_fit_percentage']}%")
    
    # Export to CSV
    csv_file = "scoring_results.csv"
    pipeline.export_results(csv_file, format="csv")
    print(f"✓ Exported to {csv_file}")


def main():
    """Run all examples."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█  CROSS-ROUND AGGREGATION ENGINE - COMPREHENSIVE EXAMPLES        █")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        # Run examples
        example_1_single_candidate()
        example_2_quick_calculation()
        example_3_batch_processing()
        example_4_different_roles()
        example_5_missing_scores()
        example_6_detailed_report()
        example_7_custom_weights()
        example_8_export_results()
        
        print("\n" + "█"*70)
        print("█  ALL EXAMPLES COMPLETED SUCCESSFULLY                       █")
        print("█"*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
