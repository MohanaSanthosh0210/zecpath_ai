# AI Screening System API Design

## Resume Upload

### Endpoint

POST /resume/upload

### Input

- Resume File (.pdf / .docx)

### Output

- Structured Resume JSON

---

## ATS Evaluation

### Endpoint

POST /ats/evaluate

### Input

- Resume JSON
- Job Description JSON

### Output

- ATS Score
- Eligibility Status

---

## Speech Processing

### Endpoint

POST /speech/transcribe

### Input

- Interview Audio

### Output

- Transcript

---

## Transcript Cleaning

### Endpoint

POST /transcript/clean

### Input

- Transcript

### Output

- Clean Transcript

---

## Answer Understanding

### Endpoint

POST /nlp/analyze

### Input

- Clean Transcript

### Output

- Intent
- Skills
- Experience
- Entities
- Confidence

---

## Screening Scoring

### Endpoint

POST /screening/score

### Input

- Structured Answer

### Output

- Question Score
- Final Screening Score

---

## Behavior Analysis

### Endpoint

POST /behavior/analyze

### Input

- Structured Answer

### Output

- Confidence
- Sentiment
- Communication Strength

---

## Screening Report

### Endpoint

POST /report/generate

### Input

- AI Analysis Results

### Output

- Recruiter Screening Report

---

## Conversation Flow

### Endpoint

POST /conversation/next

### Input

- Previous Conversation State

### Output

- Next AI Action
- Follow-up Question
- Retry
- Clarification

---

## Edge Case Handling

### Endpoint

POST /edge-case/check

### Input

- Transcript

### Output

- Retry Decision
- Clarification
- Safety Fallback

---

# API Workflow

Resume Upload
↓

ATS Evaluation
↓

Speech Processing
↓

Transcript Cleaning
↓

Answer Understanding
↓

Screening Scoring
↓

Behavior Analysis
↓

Report Generation
↓

Conversation Flow
↓

Edge Case Handling
↓

Final AI Decision