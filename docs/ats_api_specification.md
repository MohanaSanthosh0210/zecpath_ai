# ATS API Specification

## 1. Resume Upload API

### Endpoint
POST /api/v1/resumes/upload

### Request

```json
{
  "file_name": "resume.pdf"
}
```

### Response

```json
{
  "status": "success",
  "resume_id": "RES001"
}
```

---

## 2. Resume Parsing API

### Endpoint
POST /api/v1/resumes/parse

### Request

```json
{
  "resume_id": "RES001"
}
```

### Response

```json
{
  "skills": [
    "Python",
    "FastAPI"
  ],
  "experience": [
    "Software Engineer"
  ],
  "education": [
    "B.Tech Computer Science"
  ]
}
```

---

## 3. ATS Scoring API

### Endpoint
POST /api/v1/resumes/score

### Request

```json
{
  "resume_id": "RES001",
  "job_id": "JD001"
}
```

### Response

```json
{
  "final_ats_score": 87.5,
  "status": "Shortlisted"
}
```

---

## 4. Candidate Shortlisting API

### Endpoint
GET /api/v1/candidates/shortlist

### Response

```json
{
  "candidates": [
    {
      "candidate_id": "RES001",
      "score": 87.5
    }
  ]
}
```

---

# Error Response

```json
{
  "status": "error",
  "message": "Resume not found"
}
```

---

# HTTP Status Codes

| Code | Meaning |
|--------|----------|
| 200 | Success |
| 400 | Invalid Request |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

---

# Logging Standards

- INFO - Resume Uploaded
- INFO - Resume Parsed
- INFO - ATS Score Generated
- INFO - Candidate Shortlisted
- ERROR - API Processing Failed