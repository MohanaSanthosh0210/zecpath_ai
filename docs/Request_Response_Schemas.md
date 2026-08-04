# Request & Response Schemas

## Resume Parser

### Request

```json
{
    "candidate_id": "C001",
    "resume_path": "resume.pdf"
}
```

### Response

```json
{
    "candidate_id": "C001",
    "skills": [],
    "experience": 2,
    "education": "B.Tech"
}
```

---

## ATS

### Request

```json
{
    "candidate_id": "C001",
    "resume_data": {}
}
```

### Response

```json
{
    "ats_score": 85,
    "matched_skills": []
}
```

---

## Hiring Intelligence

### Response

```json
{
    "candidate_id": "C001",
    "overall_score": 88,
    "decision": "Hire"
}
```