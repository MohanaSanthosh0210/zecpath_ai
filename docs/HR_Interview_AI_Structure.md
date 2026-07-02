# HR Interview AI Structure

## Overview

The HR Interview AI module is responsible for conducting structured HR interviews with candidates. It dynamically selects questions based on the candidate's experience level and role type while maintaining a controlled interview flow.

The objective is to simulate a professional HR interview and collect structured responses for downstream AI evaluation.

---

# HR Interview Architecture

Candidate

↓

Interview Initialization

↓

Interview Category Selection

↓

Role-Based Question Generator

↓

Conversation State Manager

↓

Response Capture

↓

Follow-up Decision

↓

Next Question

↓

Interview Completion

↓

Structured Interview Output

---

# Main Components

## Interview Categories

Responsible for organizing HR interview questions into logical sections.

Categories include:

- Self Introduction
- Career Journey
- Strengths & Weaknesses
- Teamwork & Culture Fit
- Career Goals
- Availability & Commitment

---

## Role-Based Question Generator

Generates interview questions based on:

- Fresher
- Experienced

and

- Technical Roles
- Non-Technical Roles

---

## Interview State Manager

Maintains:

- Current Phase
- Current Question
- Question ID
- Candidate Response
- Follow-up Requirement
- Conversation History

---

## Conversation Controller

Controls interview progression through predefined phases:

Introduction

↓

Core HR Questions

↓

Role-Based Questions

↓

Closing

---

## Final Output

The interview engine produces a structured interview design that can later be used by the AI Interview Engine for conducting live interviews.