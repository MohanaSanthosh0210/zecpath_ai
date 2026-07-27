# Cross-Round Aggregation Engine - Documentation

## Overview

The Cross-Round Aggregation Engine combines evaluation scores from all hiring stages into a unified hiring intelligence score. It provides transparent scoring breakdowns, role-based weightage customization, and comprehensive candidate fit analysis.

## Key Features

✅ **Multi-Stage Aggregation**
- ATS (Resume Screening)
- Screening (Initial Phone Screen)
- HR Interview (Cultural Fit & Soft Skills)
- Technical Interview (Problem-Solving & Depth)
- Machine Test (Coding Ability & Execution)
- Behavioral Intelligence (Personality & Confidence)

✅ **Role-Specific Weightage**
- 10+ predefined role configurations
- Easy customization for new roles
- Per-component weight control

✅ **Transparent Scoring**
- Component-wise breakdown
- Normalization details
- Calculation notes and audit trail
- Red flags and insights

✅ **Comprehensive Candidate Profile**
- Unified score object with all metadata
- Strengths and concerns identification
- Hiring recommendations
- Missing evaluations tracking

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│          CrossRoundAggregationEngine                         │
│  - Orchestrates aggregation                                 │
│  - Applies role-based weightage                             │
│  - Normalizes scores                                        │
│  - Detects outliers                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    ┌────────┐ ┌─────────┐ ┌──────────────┐
    │Normalizer  │Outlier  │  Profile    │
    │(5 methods) │Detector │ Normalizer  │
    └────────┘ └─────────┘ └──────────────┘
        │          │          │
        └──────────┼──────────┘
                   ▼
        ┌──────────────────────┐
        │UnifiedCandidateScore │
        │- All round scores    │
        │- Weights used        │
        │- Final hiring fit %  │
        │- Insights & flags    │
        └──────────────────────┘
```

## Core Components

### 1. UnifiedCandidateScore Schema

Represents the complete hiring evaluation for a candidate.

```python
@dataclass
class UnifiedCandidateScore:
    candidate_id: str           # Unique identifier
    job_id: Optional[str]       # Position identifier
    role: str                   # Job role
    
    # All evaluations
    round_scores: Dict[str, RoundScore]
    
    # Weights applied
    weights: ScoreWeights
    
    # Final scores
    unified_score: float        # 0-100
    hiring_fit_percentage: float # 0-100
    status: HiringFitStatus     # Strong/Good/Review/Conditional/Not Fit
    
    # Transparency
    component_contributions: Dict[str, float]
    calculation_notes: List[str]
    missing_rounds: List[str]
    
    # Insights
    red_flags: List[str]
    strengths: List[str]
    concerns: List[str]
    
    # Recommendation
    recommendation: str
    decision: str               # APPROVE/REVIEW/CONDITIONAL/REJECT
```

### 2. CrossRoundAggregationEngine

Main aggregation engine with role-based customization.

**Methods:**
- `aggregate()` - Main aggregation method
- `get_weights_for_role()` - Get role-specific weights
- `validate_weights()` - Ensure weights sum to 1.0

### 3. HiringFitCalculator

Quick calculator for simple hiring fit assessments.

**Methods:**
- `calculate()` - Single candidate calculation
- `calculate_batch()` - Multiple candidates

### 4. CrossRoundScoringPipeline

End-to-end pipeline with batch processing and reporting.

**Methods:**
- `process_candidate()` - Process single candidate
- `process_batch()` - Process multiple candidates
- `generate_comparison_report()` - Compare candidates
- `export_results()` - Export to JSON/CSV

### 5. ScoreNormalizer

Normalizes scores using multiple methods:
- **Min-Max Scaling**: Linear scaling to target range
- **Z-Score**: Statistical normalization
- **Percentile**: Rank-based normalization
- **Sigmoid**: Smooth S-curve scaling
- **Robust**: Outlier-resistant using quartiles
- **Linear Interpolation**: Custom reference points

### 6. CandidateProfileNormalizer

Adjusts expectations based on:
- Experience level (0-1yr, 1-3yr, 3-5yr, 5-10yr, 10+yr)
- Background (traditional, bootcamp, self-taught, career switch)
- Geographic location (cost of living adjustment)

## Role-Based Weightage System

Predefined roles:
```json
{
  "default": {"ats": 0.20, "screening": 0.20, ...},
  "python_developer": {"ats": 0.15, "screening": 0.15, ...},
  "data_scientist": {"ats": 0.15, "screening": 0.15, ...},
  "frontend_developer": {"ats": 0.15, "screening": 0.15, ...},
  "backend_developer": {"ats": 0.15, "screening": 0.15, ...},
  "product_manager": {"ats": 0.20, "screening": 0.20, ...},
  // ... more roles
}
```

Configure in: `scoring/config/cross_round_weights.json`

## Usage Examples

### Example 1: Single Candidate Calculation

```python
from scoring.cross_round_aggregation import CrossRoundAggregationEngine

# Initialize
engine = CrossRoundAggregationEngine()

# Aggregate scores
result = engine.aggregate(
    candidate_id="CAND-001",
    role="python_developer",
    scores={
        "ats": 78,
        "screening": 82,
        "hr_interview": 75,
        "technical_interview": 88,
        "machine_test": 92,
    }
)

# Access results
print(f"Hiring Fit: {result.hiring_fit_percentage}%")
print(f"Status: {result.status.value}")
print(f"Decision: {result.decision}")
print(f"Recommendation: {result.recommendation}")
```

### Example 2: Quick Fit Calculation

```python
from scoring.cross_round_aggregation import HiringFitCalculator

calculator = HiringFitCalculator()

result = calculator.calculate(
    candidate_id="CAND-002",
    role="data_scientist",
    ats_score=75,
    screening_score=80,
    hr_interview_score=85,
    technical_interview_score=82,
    machine_test_score=78,
)

print(result["hiring_fit_percentage"])
print(result["status"])
```

### Example 3: Batch Processing

```python
from scoring.aggregation_pipeline import CrossRoundScoringPipeline

pipeline = CrossRoundScoringPipeline()

candidates = [
    {
        "candidate_id": "CAND-001",
        "role": "python_developer",
        "ats": 78, "screening": 82, "hr_interview": 75,
        "technical_interview": 88, "machine_test": 92,
    },
    {
        "candidate_id": "CAND-002",
        "role": "python_developer",
        "ats": 65, "screening": 70, "hr_interview": 72,
        "technical_interview": 68, "machine_test": 75,
    },
]

results = pipeline.process_batch(candidates)

# Generate comparison report
report = pipeline.generate_comparison_report()
print(report)

# Export results
pipeline.export_results("hiring_results.json", format="json")
```

### Example 4: Custom Weights

```python
from scoring.cross_round_aggregation import CrossRoundAggregationEngine

custom_weights = {
    "custom_role": {
        "ats": 0.10,
        "screening": 0.15,
        "hr_interview": 0.20,
        "technical_interview": 0.40,
        "machine_test": 0.15,
        "behavioral_intelligence": 0.00,
    }
}

engine = CrossRoundAggregationEngine(custom_weights=custom_weights)

result = engine.aggregate(
    candidate_id="CAND-003",
    role="custom_role",
    scores={...}
)
```

### Example 5: Detailed Report Generation

```python
from scoring.aggregation_pipeline import AggregationReportGenerator

# Single candidate report
candidate_report = AggregationReportGenerator.generate_candidate_report(result)
print(candidate_report)

# Save to file
with open("candidate_report.txt", "w") as f:
    f.write(candidate_report)

# Summary report for multiple candidates
summary = AggregationReportGenerator.generate_summary_report(results)
print(summary)
```

## Hiring Fit Status Categories

| Status | Range | Meaning |
|--------|-------|---------|
| **Strong Fit** | 85-100% | Excellent match, recommend hire |
| **Good Fit** | 70-84% | Strong match, recommend hire |
| **Requires Review** | 55-69% | Moderate match, needs evaluation |
| **Conditional Fit** | 40-54% | Limited match, junior/training option |
| **Not Fit** | 0-39% | Poor match, not recommended |

## Normalization Methods

### 1. Min-Max Scaling
Best for: Converting different scales to 0-100
```python
normalized = (value - min) / (max - min) * 100
```

### 2. Z-Score (Statistical)
Best for: Comparing across role distributions
```python
z_score = (value - mean) / std_dev
normalized = z_score * target_std + target_mean
```

### 3. Percentile
Best for: Rank-based comparisons
```python
percentile = count_below / total * 100
```

### 4. Sigmoid
Best for: Probability-like scaling
```python
sigmoid = 1 / (1 + e^(-k*(x-x0)))
normalized = sigmoid * 100
```

### 5. Robust (Using Quartiles)
Best for: Handling outliers
```python
normalized = ((value - median) / (1.35 * IQR)) mapped to range
```

## Transparency Features

### Calculation Notes
Every aggregation tracks transformation steps:
- Score normalization applied
- Outliers detected
- Weights applied per role
- Missing rounds identified

### Component Contributions
Visual breakdown of each evaluation's contribution:
```
ATS: ████░░░░░░ 15%
Screening: ████░░░░░░ 16%
HR Interview: ██████░░░░ 20%
Technical: ███████░░░░ 23%
Machine Test: ████░░░░░░ 15%
```

### Red Flags
Automatically detected issues:
- Multiple evaluation stages missing
- Weakness in multiple areas
- Inconsistent performance patterns

### Strengths & Concerns
Automatically identified insights:
- Strong performance areas (score ≥ 80)
- Weak performance areas (score < 50)

## Data Export

### JSON Format
Complete scoring breakdown with all details:
```python
pipeline.export_results("results.json", format="json")
```

### CSV Format
Flat table for spreadsheet analysis:
```python
pipeline.export_results("results.csv", format="csv")
```

## Configuration

### Role-Based Weights
File: `scoring/config/cross_round_weights.json`

Add new role:
```json
{
  "new_role": {
    "ats": 0.15,
    "screening": 0.15,
    "hr_interview": 0.25,
    "technical_interview": 0.30,
    "machine_test": 0.15,
    "behavioral_intelligence": 0.00
  }
}
```

Weights must sum to 1.0.

### Hiring Fit Thresholds
Modify in `CrossRoundAggregationEngine.FIT_THRESHOLDS`:
```python
FIT_THRESHOLDS = {
    HiringFitStatus.STRONG_FIT: 85.0,
    HiringFitStatus.GOOD_FIT: 70.0,
    HiringFitStatus.REQUIRES_REVIEW: 55.0,
    HiringFitStatus.CONDITIONAL_FIT: 40.0,
    HiringFitStatus.NOT_FIT: 0.0,
}
```

## Performance Characteristics

- **Single candidate**: ~50-100ms
- **Batch (100 candidates)**: ~5-10s
- **Memory**: ~1MB per 1000 candidates
- **Accuracy**: Supports 0.01% precision

## Integration Points

1. **With ATS Engine**
   ```python
   from scoring.ats_scoring_engine import calculate_ats_score
   ats_score = calculate_ats_score(...)
   ```

2. **With HR Scoring**
   ```python
   from hr_scoring.hr_scoring_engine import HRInterviewScoringEngine
   hr_score = HRInterviewScoringEngine().process()
   ```

3. **With Technical Interview**
   ```python
   from technical_scoring.technical_scoring_engine import TechnicalScoringEngine
   tech_score = TechnicalScoringEngine.evaluate(...)
   ```

4. **With Machine Test**
   ```python
   from machine_test_ai.report_generator import MachineTestReportGenerator
   mt_score = MachineTestReportGenerator.generate(...)
   ```

## Common Issues & Solutions

### Issue: Weights don't sum to 1.0
**Solution**: Adjust weights in config file or pass corrected weights dict

### Issue: Missing round scores cause errors
**Solution**: System handles None values gracefully; missing rounds tracked in `missing_rounds`

### Issue: Scores from different scales
**Solution**: Normalization handles conversion automatically; ensure raw scores are 0-100

### Issue: Outlier scores skewing results
**Solution**: Enable `detect_outliers=True` in aggregate() for automatic handling

## Testing

Run tests:
```bash
python -m pytest tests/test_cross_round_aggregation.py -v
```

Test coverage areas:
- Score aggregation
- Normalization methods
- Role-based weightage
- Outlier detection
- Batch processing
- Report generation

## Future Enhancements

- [ ] Machine learning-based weight optimization
- [ ] Dynamic threshold adjustment based on role history
- [ ] Trend analysis across multiple hiring cycles
- [ ] Bias detection and fairness auditing
- [ ] Integration with ATS systems
- [ ] REST API endpoints
- [ ] Real-time scoring dashboard

## Support

For issues or questions:
1. Check calculation_notes in UnifiedCandidateScore
2. Review red_flags for common issues
3. Check missing_rounds for incomplete data
4. Refer to component_contributions for weight verification
