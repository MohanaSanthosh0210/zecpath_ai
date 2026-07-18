# HR Interview AI – API Specification

## Version

1.0

---

# Overview

This document defines the API specification for integrating the HR Interview AI System with external applications.

The APIs are REST-oriented and exchange data using JSON.

---

# Base URL

```
http://localhost:8000/api/v1/
```

*(Replace with production URL after deployment.)*

---

# Authentication

All endpoints should be protected using authentication.

Example:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

# Content Type

Request

```
Content-Type: application/json
```

Response

```
application/json
```

---

# API Flow

```
Resume Upload
      │
      ▼
ATS Evaluation
      │
      ▼
Interview Session
      │
      ▼
Speech Processing
      │
      ▼
Answer Evaluation
      │
      ▼
Unified Scoring
      │
      ▼
Recruiter Report
```

---

# 1. Upload Resume

### Endpoint

```
POST /resume/upload
```

### Description

Uploads a candidate resume for ATS evaluation.

### Request

```json
{
    "candidate_id": "C001",
    "resume_file": "resume.pdf"
}
```

### Response

```json
{
    "status": "success",
    "candidate_id": "C001",
    "resume_processed": true
}
```

---

# 2. ATS Evaluation

### Endpoint

```
POST /ats/evaluate
```

### Description

Runs ATS scoring against a Job Description.

### Request

```json
{
    "candidate_id": "C001",
    "job_id": "JD001"
}
```

### Response

```json
{
    "ats_score": 84.6,
    "matched_skills": [
        "Python",
        "SQL",
        "Machine Learning"
    ]
}
```

---

# 3. Start Interview

### Endpoint

```
POST /interview/start
```

### Description

Creates a new HR interview session.

### Request

```json
{
    "candidate_id": "C001"
}
```

### Response

```json
{
    "session_id": "HR001",
    "first_question": "Tell me about yourself."
}
```

---

# 4. Submit Interview Answer

### Endpoint

```
POST /interview/answer
```

### Description

Uploads an interview response.

### Request

```json
{
    "session_id": "HR001",
    "audio_file": "answer.wav"
}
```

### Response

```json
{
    "transcription_complete": true,
    "follow_up_required": false
}
```

---

# 5. Communication Evaluation

### Endpoint

```
GET /communication/{candidate_id}
```

### Response

```json
{
    "communication_score": 91,
    "fluency": 92,
    "grammar": 88,
    "clarity": 94
}
```

---

# 6. Behaviour Analysis

### Endpoint

```
GET /behaviour/{candidate_id}
```

### Response

```json
{
    "confidence_score": 87,
    "stress_score": 18,
    "hesitation_count": 1
}
```

---

# 7. HR Interview Score

### Endpoint

```
GET /hr-score/{candidate_id}
```

### Response

```json
{
    "answer_relevance": 92,
    "communication": 91,
    "confidence": 87,
    "consistency": 90,
    "hr_score": 90.4
}
```

---

# 8. Aptitude Evaluation

### Endpoint

```
GET /aptitude/{candidate_id}
```

### Response

```json
{
    "logical_reasoning": 89,
    "problem_solving": 91,
    "scenario_score": 88,
    "aptitude_score": 89.3
}
```

---

# 9. Unified Candidate Score

### Endpoint

```
GET /candidate/unified-score/{candidate_id}
```

### Response

```json
{
    "candidate_id": "C001",
    "ats_score": 84.6,
    "screening_score": 88.2,
    "hr_score": 90.4,
    "overall_score": 88.6,
    "hiring_fit": 89.4,
    "recommendation": "Strong Hire"
}
```

---

# 10. Recruiter Report

### Endpoint

```
GET /candidate/report/{candidate_id}
```

### Response

```json
{
    "candidate_id": "C001",
    "summary": {
        "strengths": [
            "Strong communication",
            "Good logical reasoning"
        ],
        "weaknesses": [
            "Needs more structured examples"
        ],
        "culture_fit": "High",
        "risk_flags": []
    }
}
```

---

# 11. Ethics Report

### Endpoint

```
GET /candidate/ethics/{candidate_id}
```

### Response

```json
{
    "consent_verified": true,
    "fairness_status": "PASS",
    "compliance": "READY"
}
```

---

# Common Response Format

Successful Response

```json
{
    "status": "success",
    "data": {}
}
```

---

Error Response

```json
{
    "status": "error",
    "message": "Candidate not found."
}
```

---

# HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

---

# Input Data Formats

Supported Resume Formats

- PDF
- DOCX

Supported Audio Formats

- WAV
- MP3
- M4A

JSON Encoding

- UTF-8

---

# Output Formats

The APIs return JSON objects only.

Generated outputs include:

- ATS Score
- Communication Report
- Behaviour Report
- HR Interview Report
- Aptitude Report
- Unified Candidate Score
- Interview Summary
- Ethics Report

---

# Integration Sequence

```
Resume Upload

↓

ATS Evaluation

↓

Interview Start

↓

Answer Submission

↓

Communication Analysis

↓

Behaviour Analysis

↓

HR Scoring

↓

Aptitude Evaluation

↓

Unified Scoring

↓

Recruiter Report
```

---

# Future APIs

Planned future endpoints may include:

- Candidate Dashboard
- Recruiter Dashboard
- Bulk Resume Processing
- Analytics Dashboard
- Interview Scheduling
- Feedback Collection
- Candidate Ranking
- Model Monitoring

These APIs are reserved for future versions of the HR Interview AI System.