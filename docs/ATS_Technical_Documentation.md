# Zecpath ATS AI Engine – Technical Documentation

## Overview

The Applicant Tracking System (ATS) AI Engine is responsible for parsing resumes, extracting candidate information, matching resumes against job descriptions, scoring candidates, ranking applicants, and generating recruiter-friendly outputs.

The ATS pipeline processes resumes and job descriptions through multiple AI modules and produces an explainable candidate score.

---

## System Components

### Resume Processing Layer

Modules:

* pdf_reader.py
* docx_reader.py
* resume_parser.py
* resume_section_extractor.py

Responsibilities:

* Read PDF and DOCX resumes
* Extract raw text
* Normalize resume content
* Identify resume sections

---

### Information Extraction Layer

Modules:

* skill_extractor.py
* education_parser.py
* experience_parser.py

Responsibilities:

* Extract technical skills
* Extract education details
* Extract professional experience

---

### Job Description Processing Layer

Modules:

* jd_cleaner.py
* jd_parser.py
* jd_extractor.py

Responsibilities:

* Clean job descriptions
* Extract required skills
* Extract experience requirements
* Extract education requirements

---

### Matching Layer

Modules:

* semantic_matching.py
* education_relevance.py
* experience_relevance.py

Responsibilities:

* Compare resume against JD
* Compute similarity scores
* Calculate relevance

---

### ATS Scoring Layer

Modules:

* ats_scoring_engine.py
* generate_candidate_score.py

Responsibilities:

* Generate ATS score
* Calculate weighted scores
* Produce final candidate ranking

---

### Ranking Layer

Modules:

* ranking_engine.py
* shortlist_engine.py

Responsibilities:

* Rank candidates
* Generate recruiter shortlist

---

### Fairness Layer

Modules:

* bias_detector.py
* resume_normalizer.py
* score_normalizer.py

Responsibilities:

* Reduce hiring bias
* Normalize scores
* Improve fairness
