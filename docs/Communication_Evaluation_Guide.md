# Communication Evaluation Guide

## Purpose

The Communication Evaluation module objectively measures how effectively a candidate communicates during the AI interview.

Rather than relying on subjective recruiter opinions, the system evaluates measurable communication characteristics and produces a normalized communication score.

---

# Evaluation Workflow

Candidate Audio

↓

Speech-to-Text

↓

Answer Understanding

↓

structured_answer.text

↓

Communication Evaluation

↓

Communication Report

---

# Evaluation Criteria

## Fluency

Measures:

- Continuous speaking
- Smooth explanation
- Sentence flow
- Speaking consistency

---

## Grammar

Measures:

- Capitalization
- Punctuation
- Basic grammatical correctness

---

## Vocabulary

Measures:

- Vocabulary richness
- Word diversity
- Appropriate terminology

---

## Clarity

Measures:

- Complete explanations
- Sentence organization
- Supporting details
- Logical communication

---

## Filler Words

Detects unnecessary words including:

- um
- uh
- actually
- basically
- like
- you know

Lower filler usage results in higher communication quality.

---

## Answer Structure

Evaluates whether the candidate provides:

Introduction

↓

Supporting Explanation

↓

Conclusion

Even when a conclusion is absent, partial structure credit is awarded for logically organized responses.

---

# Communication Score

The AI combines all component scores into a normalized communication score ranging from 0 to 100.

Higher scores indicate stronger communication ability.

---

# Generated Output

The Communication Evaluation module automatically reads the candidate answer from:

data/understood_answers/sample_answer.json

using:

structured_answer.text

It then generates:

- Fluency Score
- Grammar Score
- Vocabulary Score
- Clarity Score
- Filler Word Score
- Structure Score
- Overall Communication Score

The evaluation report is automatically saved to:

data/communication/communication_score.json

---

# Integration with AI Screening Pipeline

The Communication Evaluation module is fully integrated with the overall AI Screening System.

Audio

↓

Speech-to-Text

↓

Answer Understanding

↓

Communication Evaluation

↓

HR Evaluation

↓

Final AI Screening Decision

This integration allows communication quality to contribute directly to the overall candidate evaluation.