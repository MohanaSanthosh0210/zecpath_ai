# Communication Scoring Formula

## Overview

The Communication Score is calculated using multiple communication quality metrics.

Each metric contributes a weighted percentage to produce a normalized communication score between 0 and 100.

---

# Scoring Components

| Component | Weight |
|-----------|-------:|
| Fluency | 20% |
| Grammar | 20% |
| Vocabulary | 15% |
| Clarity | 15% |
| Filler Words | 15% |
| Answer Structure | 15% |

---

# Formula

Communication Score =

(Fluency × 0.20)

+

(Grammar × 0.20)

+

(Vocabulary × 0.15)

+

(Clarity × 0.15)

+

(Filler Score × 0.15)

+

(Structure Score × 0.15)

---

# Example Calculation

Fluency = 100

Grammar = 100

Vocabulary = 95

Clarity = 95

Filler Score = 100

Structure = 70

Communication Score

=

(100 × 0.20)

+

(100 × 0.20)

+

(95 × 0.15)

+

(95 × 0.15)

+

(100 × 0.15)

+

(70 × 0.15)

=

94.75

---

# Score Interpretation

| Score | Interpretation |
|--------|----------------|
| 90–100 | Excellent Communication |
| 80–89 | Very Good Communication |
| 70–79 | Good Communication |
| 60–69 | Average Communication |
| Below 60 | Needs Improvement |

---

# Bias Reduction Strategy

To improve fairness, the Communication Scoring Model:

- Uses objective measurable metrics
- Does not evaluate accent
- Does not penalize speaking style
- Focuses on communication quality
- Uses weighted normalization
- Produces consistent scores across candidates

---

# Input Source

The Communication Evaluator automatically reads the candidate response from:

data/understood_answers/sample_answer.json

using:

structured_answer.text

No manual response entry is required.