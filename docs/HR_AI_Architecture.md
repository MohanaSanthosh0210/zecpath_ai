# HR Interview AI – System Architecture

## Version

1.0

---

# Overview

The HR Interview AI System is an end-to-end AI-powered recruitment platform designed to automate candidate screening, HR interview evaluation, aptitude assessment, and hiring recommendation generation.

The system combines resume analysis, conversational AI, communication evaluation, behavioral analysis, aptitude scoring, unified hiring intelligence, optimization, and ethics review into a single recruitment pipeline.

---

# High-Level Architecture

```
                    Resume Upload
                          │
                          ▼
                 Resume Processing Engine
                          │
                          ▼
                    ATS Scoring Engine
                          │
                          ▼
              Interview Question Generator
                          │
                          ▼
                 Speech-to-Text Engine
                          │
                          ▼
                Answer Understanding Engine
                          │
                          ▼
              Dynamic Follow-up Question Engine
                          │
                          ▼
        Communication Evaluation (Day 35)
                          │
                          ▼
 Confidence & Behaviour Analysis (Day 36)
                          │
                          ▼
            HR Interview Scoring (Day 37)
                          │
                          ▼
        Aptitude Logic Evaluation (Day 38)
                          │
                          ▼
         Interview Summary Generator (Day 39)
                          │
                          ▼
      End-to-End Interview Simulation (Day 40)
                          │
                          ▼
         Unified Hiring Intelligence (Day 41)
                          │
                          ▼
     Optimization & Stability Layer (Day 42)
                          │
                          ▼
       Ethics & Compliance Review (Day 43)
                          │
                          ▼
             Final Recruiter Report
```

---

# System Modules

## 1. Resume Processing

Responsibilities

- Resume Parsing
- OCR
- Skill Extraction
- Experience Extraction
- Education Extraction
- Resume Cleaning

Outputs

- Structured Resume JSON
- Candidate Profile

---

## 2. ATS Engine

Responsibilities

- Resume-JD Matching
- Semantic Similarity
- Keyword Matching
- Resume Ranking

Outputs

- ATS Score
- Resume Ranking
- Skill Match Report

---

## 3. HR Interview Engine

Responsibilities

- Interview Question Selection
- Dynamic Follow-up Questions
- Intent Detection
- Candidate Response Understanding

Outputs

- Structured Interview Responses

---

## 4. Communication Evaluation

Responsibilities

- Fluency Analysis
- Grammar Evaluation
- Vocabulary Assessment
- Clarity Detection
- Filler Word Detection
- Answer Structure Analysis

Outputs

- Communication Score

---

## 5. Behaviour Analysis

Responsibilities

- Confidence Detection
- Hesitation Detection
- Sentiment Analysis
- Stress Indicators
- Contradiction Detection

Outputs

- Behaviour Confidence Score

---

## 6. HR Interview Scoring

Responsibilities

- Answer Relevance
- Communication Integration
- Confidence Integration
- Consistency Evaluation

Outputs

- HR Interview Score

---

## 7. Aptitude Evaluation

Responsibilities

- Logical Reasoning
- Scenario Evaluation
- Problem Solving
- Answer Pattern Analysis

Outputs

- Aptitude Score

---

## 8. Interview Summary

Responsibilities

- Strength Analysis
- Weakness Analysis
- Risk Flag Detection
- Culture Fit Analysis

Outputs

- Recruiter Summary Report

---

## 9. Unified Scoring Engine

Responsibilities

Combine

- ATS Score
- Screening Score
- HR Interview Score

Outputs

- Unified Candidate Score
- Hiring Fit Percentage

---

## 10. Optimization Layer

Responsibilities

- Reduce False Positives
- Reduce False Negatives
- Transcript Cleanup
- Scoring Optimization
- Performance Optimization

Outputs

- Stable AI Pipeline

---

## 11. Ethics & Compliance

Responsibilities

- Consent Verification
- Fairness Audit
- Explainability
- Compliance Verification

Outputs

- Ethics Report
- Fairness Report
- Compliance Report

---

# Folder Structure

```
project/

resume_processing/

ats/

speech_processing/

screening/

communication_evaluation/

behavioral_intelligence/

hr_scoring/

aptitude_evaluation/

interview_reporting/

interview_simulation/

unified_scoring/

optimization/

ethics_compliance/

docs/

tests/

config/

data/
```

---

# Data Flow

```
Resume

↓

Resume Parser

↓

ATS Engine

↓

Interview Engine

↓

Speech-to-Text

↓

Answer Understanding

↓

Follow-up Engine

↓

Communication

↓

Behaviour

↓

HR Score

↓

Aptitude

↓

Interview Summary

↓

Unified Score

↓

Optimization

↓

Ethics Review

↓

Recruiter Report
```

---

# Input Data

The system accepts

- PDF Resume
- DOCX Resume
- Audio Responses
- Job Description
- Candidate Metadata

---

# Output Data

The system generates

- ATS Report
- Candidate Profile
- Communication Report
- Behaviour Report
- HR Score Report
- Aptitude Report
- Unified Candidate Score
- Hiring Recommendation
- Recruiter Summary
- Ethics Report

---

# Technology Stack

Programming Language

- Python

Natural Language Processing

- spaCy
- Sentence Transformers
- Transformers

Machine Learning

- Scikit-learn

Speech Processing

- Whisper

Data Storage

- JSON

Testing

- PyTest

---

# Processing Pipeline

```
Resume
↓

ATS

↓

Interview

↓

Communication

↓

Behaviour

↓

HR

↓

Aptitude

↓

Summary

↓

Unified Scoring

↓

Optimization

↓

Ethics Review

↓

Final Hiring Decision
```

---

# Design Principles

The HR Interview AI has been designed using the following principles:

- Modular architecture
- Explainable AI
- Ethical AI
- Configurable scoring
- Role-based evaluation
- Human-in-the-loop decision making
- Scalable processing pipeline
- Maintainable code structure

---

# System Outputs

The final output of the system consists of:

- Candidate ATS Score
- HR Interview Score
- Aptitude Score
- Unified Hiring Score
- Hiring Fit Percentage
- Recruiter Recommendation
- Interview Summary
- Ethics & Compliance Report

These outputs provide recruiters with a comprehensive and explainable assessment of each candidate.