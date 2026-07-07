# Candidate HR Score Report Format

## Overview

After HR Interview Scoring completes, the system automatically generates a structured HR Interview Report.

Location:

data/hr_scoring/hr_score_report.json

---

# Report Structure

```json
{
    "candidate_id": "UNKNOWN",

    "interview_questions": 1,

    "score_breakdown": {

        "answer_relevance": 100,

        "communication_score": 94.75,

        "confidence_score": 92.69,

        "consistency_score": 100

    },

    "weights": {

        "relevance": 0.35,

        "communication": 0.25,

        "confidence": 0.25,

        "consistency": 0.15

    },

    "weighted_score": 96.11,

    "normalized_score": 96.11,

    "final_hr_score": 96.11,

    "recommendation": "Strong Hire"
}
```

---

# Report Sections

## Candidate Information

Contains:

- Candidate ID
- Number of Interview Questions

---

## Score Breakdown

Displays individual evaluation scores for:

- Answer Relevance
- Communication
- Confidence
- Consistency

---

## Weight Configuration

Shows the exact weight applied to each evaluation component.

This provides complete explainability.

---

## Weighted Score

The combined score before normalization.

---

## Normalized Score

Adjusted score allowing fair comparison between interviews containing different numbers of questions.

---

## Final HR Score

Final normalized HR Interview Score.

Range:

0–100

---

## Recommendation

Generated automatically.

Rules:

| Score | Recommendation |
|--------|----------------|
| 85–100 | Strong Hire |
| 70–84 | Hire |
| 60–69 | Review |
| Below 60 | Reject |

---

# Usage

The HR Interview Report supports:

- Candidate Ranking
- Shortlisting
- Hiring Decisions
- Recruitment Dashboards
- HR Analytics

The report is designed to be both machine-readable and recruiter-friendly.