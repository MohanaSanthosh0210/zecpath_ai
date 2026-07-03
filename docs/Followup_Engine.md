# Follow-Up Engine

## Overview

The Follow-Up Engine enables the AI interviewer to dynamically generate follow-up questions based on candidate responses instead of asking a fixed sequence of questions.

The objective is to improve interview quality by encouraging candidates to provide complete, detailed, and meaningful answers.

---

# Engine Workflow

Candidate Answer

↓

Response Analysis

↓

Vague Answer Detection

↓

Difficulty Adaptation

↓

Repetition Check

↓

Follow-up Question Selection

↓

Conversation Update

---

# Components

## Vague Answer Detector

Responsible for detecting:

- Incomplete responses
- Very short responses
- Uncertain language
- Generic statements

Examples

- "Maybe..."
- "I don't know."
- "Not sure."

---

## Follow-Up Trigger

Determines the most suitable follow-up type.

Possible follow-up categories:

- Clarification
- Deepening
- Example-Based Prompt

---

## Difficulty Adapter

Adjusts interview depth according to candidate performance.

Simple Answer

↓

Deepening Question

Good Answer

↓

Clarification

Excellent Answer

↓

Scenario-Based Question

---

## Repetition Detector

Ensures the interviewer does not repeatedly ask the same follow-up question.

If a duplicate question is detected, the engine automatically selects the next best alternative.

---

## Conversation Tracker

Maintains:

- Question history
- Candidate responses
- Conversation progress
- Follow-up decisions

---

# Output

The Follow-Up Engine produces:

- Selected follow-up type
- Suggested follow-up question
- Difficulty level
- Conversation history
- Decision summary