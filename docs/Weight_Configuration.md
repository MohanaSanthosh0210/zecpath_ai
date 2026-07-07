# Weight Configuration System

## Overview

The HR Interview Scoring Engine uses configurable weights stored outside the source code.

This allows HR teams to adjust scoring criteria without modifying the application logic.

---

# Configuration File

Location:

hr_scoring/config/scoring_weights.json

---

# Default Configuration

```json
{
    "relevance": 0.35,
    "communication": 0.25,
    "confidence": 0.25,
    "consistency": 0.15
}
```

---

# Weight Description

| Component | Weight |
|-----------|--------|
| Answer Relevance | 35% |
| Communication | 25% |
| Confidence | 25% |
| Consistency | 15% |

---

# Validation

Before scoring begins, the configuration loader validates that:

Total Weight = 1.00

Invalid configurations automatically raise an exception.

---

# Final Formula

Final HR Score

=

(Answer Relevance × Relevance Weight)

+

(Communication × Communication Weight)

+

(Confidence × Confidence Weight)

+

(Consistency × Consistency Weight)

---

# Advantages

External configuration provides:

- Easy tuning
- Different hiring strategies
- Role-specific weight profiles
- Transparent scoring
- No code modification required