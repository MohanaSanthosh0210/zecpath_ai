# Improvement Backlog

## Issue 1: Semantic Matching Accuracy

Problem:

Current semantic matching uses TF-IDF based similarity.

Impact:

Related skills and job titles may not always be matched correctly.

Proposed Solution:

Upgrade semantic matching to Sentence Transformers or BERT embeddings.

Priority:

High

---

## Issue 2: Skill Synonym Detection

Problem:

Different representations of the same skill may not match.

Examples:

* ML vs Machine Learning
* JS vs JavaScript

Proposed Solution:

Implement skill synonym normalization dictionary.

Priority:

High

---

## Issue 3: Education Extraction

Problem:

Some degree names may not be extracted correctly.

Proposed Solution:

Expand education parsing rules and degree mappings.

Priority:

Medium

---

## Issue 4: Small Evaluation Dataset

Problem:

Current testing dataset contains only a limited number of resumes and job descriptions.

Proposed Solution:

Create a larger benchmark dataset covering multiple industries and experience levels.

Priority:

Medium

---

## Issue 5: Fairness Monitoring

Problem:

Bias indicators are not currently tracked.

Proposed Solution:

Add fairness and bias evaluation dashboards.

Priority:

Low

---

## Issue 6: Recruiter Feedback Loop

Problem:

ATS cannot currently learn from recruiter decisions.

Proposed Solution:

Capture recruiter actions and use them to refine scoring weights.

Priority:

Low
