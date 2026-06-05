# Semantic Matching Accuracy Report

## Overview

This report documents the current semantic matching engine in `scoring/semantic_matching.py`.
It describes the available test data and job types, how threshold tuning works, current validation coverage, and example resume ↔ job description pairs.

## Engine Summary

The semantic matching engine uses TF-IDF embeddings and cosine similarity to compare:
- Skills
- Experience summaries
- Project descriptions

The final score is a weighted aggregate of:
- `skills_similarity`
- `experience_similarity`
- `project_similarity`

The engine also supports threshold tuning using labeled resume/JD pairs.

## Test Data and Job Types

### Available validation examples

Current repository validation is based on unit test examples in `tests/test_semantic_matching.py`.

Example job types covered by these tests:
- Senior Cloud Engineer / Senior Software Engineer
- Backend Developer / Backend Engineer

### Resume and job profiles used in tests

1. Senior Cloud Engineer matching:
   - Resume skills: Python, AWS, Kubernetes
   - Resume experience: cloud-native applications, AWS, Kubernetes cluster management
   - Resume project: cloud migration, CI/CD automation
   - JD title: Senior Cloud Engineer
   - JD description: Python, AWS, Kubernetes infrastructure operations
   - JD required skills: Python, AWS, Kubernetes
   - JD project: legacy-to-cloud migration, deployment automation

2. Backend Developer matching:
   - Resume skills: Python, Django, AWS
   - Resume experience: REST APIs, Django, AWS deployments
   - Resume projects: API development and AWS deployment
   - JD title: Backend Developer
   - JD description: Build REST APIs with Python and Django, deploy to AWS
   - JD required skills: Python, Django, AWS
   - JD projects: REST API development

Negative pairing example:
   - Resume skills: Graphic Design, Photoshop
   - Resume experience: visual asset creation, branding
   - JD title: Backend Developer
   - JD description: Build REST APIs with Python and Django, deploy to AWS

## Threshold Tuning Results

The engine uses default thresholds defined in `SemanticMatchingEngine.__init__`:
- `skills`: 0.55
- `experience`: 0.20
- `projects`: 0.02
- `overall`: 0.45

### Tuning behavior

The `tune_thresholds()` method evaluates labeled positive and negative resume/JD pairs and updates `overall` to a midpoint between the positive and negative mean scores, constrained to the range [0.2, 0.9].

### Example from tests

The unit test `test_semantic_matching_tunes_thresholds_with_labels()` verifies that:
- `tune_thresholds()` returns an `overall` threshold between `0.2` and `0.9`
- the engine updates `engine.thresholds["overall"]` to the tuned value

This demonstrates the tuning mechanism without a full labeled dataset.

## Matching Accuracy

### Current evaluation status

A complete precision/recall report is not available in the repository because there is no labeled production dataset with broad resume/JD relevance labels.

### Validation method

Current validation is performed with unit tests that assert:
- `skills_similarity` is above expected semantic similarity when resumes are relevant
- `experience_similarity` is above the experience threshold
- `project_similarity` is above the project threshold
- `overall_similarity` is above the overall threshold
- `match == True` for relevant pairs

These unit tests serve as functional accuracy checks for the engine.

### Accuracy metrics roadmap

To produce formal precision/recall or matching accuracy metrics, the following would be required:
- a labeled dataset of resume/JD pairs with relevance judgments
- a scoring threshold decision rule for match vs non-match
- calculation of true positives, false positives, true negatives, and false negatives
- derived metrics such as precision, recall, F1 score, and overall accuracy

## Examples of Resume ↔ JD Pairs

### Example 1: Cloud Engineer

Resume data:
```python
resume_profile = {
    "skills": ["Python", "AWS", "Kubernetes"],
    "experience": [
        {
            "designation": "Senior Software Engineer",
            "responsibilities": [
                "Built and deployed cloud-native applications with Python and AWS.",
                "Managed Kubernetes clusters for production services.",
            ],
        }
    ],
    "projects": [
        {
            "description": "Migrated monolith to AWS ECS, added CI/CD pipelines, and reduced deployment time by 60%."
        }
    ],
}
```

Job profile:
```python
job_profile = {
    "job_title": "Senior Cloud Engineer",
    "job_description": "Seeking an experienced engineer with strong Python, AWS, and Kubernetes experience to operate cloud infrastructure.",
    "required_skills": ["Python", "AWS", "Kubernetes"],
    "projects": [
        {
            "description": "Lead the migration of legacy systems to cloud infrastructure and improve deployment automation."
        }
    ],
}
```

Expected behavior:
- `match == True`
- `skills_similarity >= 0.7`
- `experience_similarity >= 0.2`
- `project_similarity >= 0.02`
- `overall_similarity >= 0.45`

### Example 2: Backend Developer vs Graphic Designer

Positive case resume:
```python
resume_profile = {
    "skills": ["Python", "Django", "AWS"],
    "experience": [
        {
            "designation": "Backend Engineer",
            "responsibilities": [
                "Developed REST APIs using Django and deployed services to AWS."
            ],
        }
    ],
    "projects": ["API development and AWS deployment"],
}
```

Job profile:
```python
job_profile = {
    "job_title": "Backend Developer",
    "job_description": "Build REST APIs with Python and Django, deploy to AWS.",
    "required_skills": ["Python", "Django", "AWS"],
    "projects": ["REST API development"],
}
```

Negative case resume:
```python
resume_profile = {
    "skills": ["Graphic Design", "Photoshop"],
    "experience": [
        {
            "designation": "Graphic Designer",
            "responsibilities": [
                "Created visual assets and branding materials using Photoshop."
            ],
        }
    ],
    "projects": ["Brand identity refresh"],
}
```

Expected behavior for positive case:
- `match == True`

Expected behavior for negative case:
- `match == False`

## Notes

- The current semantic matching implementation is TF-IDF-based rather than neural embedding-based.
- The engine and report can be extended later once a broader labeled dataset is available.