# Sentiment Scoring Engine

## Overview

The Sentiment Scoring Engine evaluates the emotional tone of the candidate's response.

It performs lightweight rule-based sentiment analysis suitable for AI interview evaluation.

---

# Input

The engine reads:

structured_answer.text

from:

data/understood_answers/sample_answer.json

---

# Positive Signals

Examples include:

- achieved
- improved
- developed
- implemented
- built
- completed
- confident
- learned
- managed
- delivered
- success

---

# Negative Signals

Examples include:

- failed
- failure
- problem
- difficult
- confused
- worried
- stress
- panic
- unable

---

# Sentiment Classification

The engine classifies responses into:

Positive

Neutral

Negative

based on the normalized sentiment score.

---

# Output

Example:

{
    "positive_signals": 2,
    "negative_signals": 0,
    "sentiment_score": 70,
    "sentiment": "Positive"
}

The sentiment result contributes to both:

- Stress estimation
- Behavioral Confidence Score