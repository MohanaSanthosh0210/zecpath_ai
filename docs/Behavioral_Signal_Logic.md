# Behavioral Signal Logic

## Overview

The Behavioral Intelligence module combines multiple behavioral indicators to estimate the candidate's confidence during an AI interview.

The module integrates outputs from previous stages of the AI screening pipeline.

---

# Pipeline

Candidate Audio

↓

Speech-to-Text (Day 24)

↓

Answer Understanding (Day 25)

↓

structured_answer.text

↓

Communication Evaluation (Day 35)

↓

communication_score.json

↓

Behavioral Intelligence (Day 36)

↓

behavioral_report.json

---

# Behavioral Components

The Behavioral Intelligence Engine evaluates:

- Confidence
- Sentiment
- Contradictions
- Stress
- Communication

---

# Confidence Formula

Confidence Score

=

100

−

(Hesitation Count × 10)

−

(Repeated Words × 5)

---

# Stress Formula

Stress Score

=

(Hesitation Count × 10)

+

(Repeated Words × 5)

+

20 (if sentiment is Negative)

The stress score is capped at 100.

---

# Contradiction Detection

The engine compares the structured information extracted during Day 25 with the candidate's spoken response.

Examples:

- Experience conflict
- Availability conflict
- Salary expectation conflict

Each contradiction reduces the contradiction score.

---

# Behavioral Confidence Formula

The final Behavioral Confidence Score is calculated using weighted metrics:

Behavioral Confidence

=

(Confidence Score × 0.40)

+

(Communication Score × 0.25)

+

(Sentiment Score × 0.15)

+

((100 − Stress Score) × 0.10)

+

(Contradiction Score × 0.10)

---

# Output

The engine automatically generates:

data/behavioral_analysis/behavioral_report.json

Example:

{
    "candidate_id": "UNKNOWN",

    "confidence": {
        "confidence_score": 90,
        "hesitation_count": 1,
        "repeated_words": 0
    },

    "sentiment": {
        "positive_signals": 2,
        "negative_signals": 0,
        "sentiment_score": 70,
        "sentiment": "Positive"
    },

    "contradictions": {
        "count": 0,
        "contradiction_score": 100
    },

    "stress": {
        "stress_score": 10
    },

    "communication_score": 94.75,

    "behavioral_confidence_score": 91.88
}

---

# Integration with AI Screening

The Behavioral Intelligence module is fully integrated into the AI screening pipeline.

The generated Behavioral Confidence Score can be used by later modules such as:

- HR Interview Evaluation
- Final Candidate Ranking
- AI Hiring Decision Engine

This enables the AI platform to consider not only technical responses but also the candidate's behavioral confidence during decision making.