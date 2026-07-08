# Aptitude AI Design

## Objective

The Aptitude AI module evaluates a candidate's logical reasoning,
problem-solving ability, and situational judgment during an AI-driven
interview.

Unlike traditional aptitude tests, the module analyzes spoken
responses generated during the interview pipeline and produces an
explainable aptitude evaluation.

---

# System Workflow

Candidate Response

↓

Speech-to-Text (Day 24)

↓

Answer Understanding (Day 25)

↓

Communication Evaluation (Day 35)

↓

Behavioral Confidence (Day 36)

↓

HR Interview Scoring (Day 37)

↓

Aptitude Evaluation (Day 38)

---

# Core Components

## Reasoning Question Engine

Loads reasoning and situational interview questions.

Responsibilities

- Load interview scenarios
- Select reasoning questions
- Provide evaluation keywords

---

## Logical Reasoning Scorer

Measures how well the candidate addresses the expected reasoning
points.

Evaluates

- Keyword coverage
- Logical completeness
- Answer relevance

---

## Scenario Evaluator

Measures candidate performance in situational judgment questions.

Evaluates

- Situation understanding
- Decision quality
- Response completeness

---

## Problem Solving Analyzer

Detects structured problem-solving patterns.

Looks for

- Analysis
- Planning
- Solution proposal
- Implementation thinking

---

## Answer Pattern Mapper

Identifies whether the candidate follows a logical explanation
structure.

Checks

- Problem identification
- Reasoning
- Solution
- Outcome

---

# Output

The module generates

data/aptitude/aptitude_report.json

containing

- Logical reasoning score
- Scenario evaluation
- Problem-solving score
- Answer pattern score
- Final aptitude score

---

# Future Enhancement

The module will integrate directly with the Interview Session Manager
to evaluate the active interview question instead of using a static
question bank.