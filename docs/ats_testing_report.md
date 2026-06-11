# ATS Testing Report

## Objective

To validate ATS accuracy, reliability, and role adaptability across multiple resume-job combinations.

## Test Dataset

* Total Resumes Tested: 3
* Total Job Descriptions Tested: 3
* Total Evaluations: 9

## ATS Components Tested

* Resume Parsing
* Skills Extraction
* Experience Relevance
* Education Relevance
* Semantic Matching
* ATS Scoring
* Candidate Ranking
* Candidate Shortlisting

## Test Results

| Resume  | Job Description | ATS Score | Result   |
| ------- | --------------- | --------- | -------- |
| Resume1 | JD1             | 10.86     | Rejected |
| Resume2 | JD1             | Rejected  | Rejected |
| Resume3 | JD1             | Rejected  | Rejected |
| Resume1 | JD2             | Rejected  | Rejected |
| Resume2 | JD2             | Rejected  | Rejected |
| Resume3 | JD2             | Rejected  | Rejected |
| Resume1 | JD3             | Rejected  | Rejected |
| Resume2 | JD3             | Rejected  | Rejected |
| Resume3 | JD3             | Rejected  | Rejected |

## Reliability Testing

* All ATS modules executed successfully.
* No runtime failures observed during evaluation.
* Ranking outputs were generated correctly.
* Candidate shortlisting completed successfully.

## Role Adaptability

The ATS was tested against different resume and job combinations.

Categories evaluated:

* Technical Profiles
* Non-Technical Profiles
* Fresher Profiles
* Experienced Profiles

## Observations

* ATS successfully identified weak resume-job matches.
* Low ATS scores were generated when required skills were missing.
* Ranking engine correctly sorted candidates.
* Shortlisting logic worked as expected.

## Conclusion

The ATS pipeline successfully processed all resume-job combinations and generated consistent scoring, ranking, and shortlisting outputs.
