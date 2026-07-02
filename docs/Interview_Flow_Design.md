# Interview Flow Design

## Overview

The Interview Flow controls how the AI interviewer progresses through different interview stages while maintaining interview state.

---

# Interview Phases

## Phase 1 — Introduction

Purpose

- Welcome candidate
- Build rapport
- Ask self-introduction

Example

- Tell me about yourself.

---

## Phase 2 — Core HR Questions

Purpose

Evaluate:

- Career Journey
- Strengths
- Weaknesses
- Teamwork
- Career Goals
- Availability

---

## Phase 3 — Role-Based Evaluation

Purpose

Generate questions according to:

- Fresher / Experienced
- Technical / Non-Technical

Examples

Technical

- Explain your recent project.

Non-Technical

- Describe a difficult customer interaction.

---

## Phase 4 — Closing

Purpose

- Candidate questions
- Thank candidate
- End interview

Example

Do you have any questions for us?

---

# Interview State

The system continuously stores:

- Current Phase
- Question ID
- Current Question
- Candidate Response
- Follow-up Requirement
- Conversation History

---

# Follow-Up Logic

If response is too short

↓

Ask follow-up question

Else

↓

Move to next question

---

# Overall Interview Flow

Interview Start

↓

Introduction

↓

Core HR Questions

↓

Role-Based Questions

↓

Closing

↓

Interview Complete

↓

Structured Interview Output