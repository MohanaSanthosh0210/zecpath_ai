\# Zecpath AI Platform



The Zecpath AI Platform is a modular, AI-driven system designed to automate and optimize recruitment workflows, including ATS parsing, candidate screening, and interview analysis.



\## Project Structure

\- `ats\_engine/`: Logic for parsing and analyzing resumes.

\- `screening\_ai/`: AI models for candidate screening.

\- `interview\_ai/`: Tools for managing and analyzing interviews.

\- `scoring/`: Scoring algorithms for candidate evaluation.

\- `utils/`: Helper functions and logging systems.

\- `tests/`: Unit and integration tests.



\## Setup Instructions

1\. Clone this repository.

2\. Create a virtual environment: `python -m venv venv`

3\. Activate the environment: `.\\venv\\Scripts\\activate`

4\. Install requirements: `pip install -r requirements.txt`

## Unified Scoring Engine

The platform now includes a unified hiring intelligence score that combines ATS, screening, and HR interview results into a single candidate score object.

Use it with:

```python
from scoring.unified_scoring_engine import calculate_unified_score

result = calculate_unified_score(
    role="python developer",
    ats_score=85,
    screening_score=78,
    hr_score=82,
    candidate_id="C100",
    job_id="J100",
)
```

It returns a score object containing:
- round-level scores for ATS, screening, and HR interview
- role-based weighting adjustments
- a hiring-fit percentage
- a status label such as Strong Fit or Needs Review

## HR Interview Demo & Finalization

The final HR interview module is ready for stakeholder review.

Run the components with:
- python hr_interview/hr_interview_runner.py
- python hr_scoring/hr_runner.py
- python hr_interview/demo_runner.py

Generated artifacts are written under data/hr_interview/ and include demo_dataset.json, manager_evaluation_feedback.json, and final_demo_report.json.

\## License

This project is proprietary to Zecpath.

