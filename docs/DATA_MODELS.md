# Data Models & Storage

This document describes the main data artifacts used by the platform and where to find their canonical representations in the repo.

Primary data directories
- `data/sectioned_resumes/` — structured resume JSON objects consumed by `main.py` and semantic matching.
- `data/structured_jobs/` — job description JSON files (example: `jd1.json`).
- `data/semantic_matches/` — output for semantic matching and resume scoring.
- `data/understood_answers/`, `data/communication/`, `data/behavioral_analysis/` — intermediate results used by scoring engines.

Config & rule files
- `config/eligibility_rules.json` — eligibility criteria used by screening/ATS modules.

Schema modules
- Python schema files are located under `schemas/` (for example, `schemas/scoring_weights.py`). Use these as the canonical in-code schemas and to generate examples for API contracts.

Example resume JSON (minimal)
```
{
  "file_name": "resume1.pdf",
  "skills": ["python", "ml"],
  "experience": [{"company":"ACME","role":"Data Scientist","years":3}],
  "education": [{"degree":"MSc","field":"CS","year":2018}]
}
```

Example scoring output (semantic_matches/resume_scores.json)
```
{
  "job_profile": {...},
  "results": [
    {"resume_file":"resume1.json","score":87.5}
  ]
}
```

Guidance
- Keep JSON artifacts UTF-8 encoded and validate against schema modules when possible.
- When introducing new persistent artifacts, add a sample file under `data/examples/` and document its format here.
