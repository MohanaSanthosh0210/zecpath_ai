# Interview Flow Design

Version: 2.0

---

# Objective

Define the interview state machine used throughout the Technical Interview AI.

---

# Interview State Machine

START

↓

INTRODUCTION

↓

EXPERIENCE_DISCUSSION

↓

CONCEPTUAL_QUESTIONS

↓

PRACTICAL_QUESTIONS

↓

SCENARIO_BASED

↓

TECHNICAL_EVALUATION

↓

SUMMARY

↓

END

---

# State Descriptions

## INTRODUCTION

Collect

- Candidate Name
- Role
- Experience

---

## EXPERIENCE_DISCUSSION

Determine

- Candidate Experience Level
- Previous Projects
- Technical Exposure

---

## CONCEPTUAL_QUESTIONS

Evaluate

- Programming Concepts
- Framework Knowledge
- Database Concepts
- Computer Science Fundamentals

---

## PRACTICAL_QUESTIONS

Evaluate

- Coding Ability
- API Design
- Database Queries
- Debugging

---

## SCENARIO_BASED

Evaluate

- Engineering Decisions
- Optimization
- Scalability
- Architecture

---

## TECHNICAL_EVALUATION

Future modules will calculate

- Technical Accuracy
- Logical Thinking
- Problem Solving
- Coding Quality

---

## SUMMARY

Generate

- Technical Strengths
- Weaknesses
- Technical Score
- Hiring Recommendation

---

# Runtime Components

The interview session is managed using:

InterviewContext

Stores:

- Candidate Information
- Current Stage
- Current Question
- Scores
- Asked Questions

InterviewFlow

Controls transitions between interview states.

RoleMapper

Determines technical domains.

ExperienceEngine

Determines interview depth.

DifficultyEngine

Controls difficulty progression.

---

# Design Principles

The Technical Interview AI is designed to be:

- Modular
- Configuration Driven
- Role Aware
- Experience Aware
- Difficulty Adaptive
- Scalable
- Maintainable

New roles, technologies, interview stages, and question banks can be added by updating configuration files without modifying the interview engine.