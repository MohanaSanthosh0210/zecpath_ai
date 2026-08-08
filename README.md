\# Zecpath AI Platform

## Final Internship Submission

The Zecpath AI Platform is a modular, AI-driven recruitment intelligence system designed to automate and optimize hiring workflows. It brings together resume parsing, semantic matching, candidate screening, interview analysis, scoring, and reporting into a single reusable platform for HR and recruiting use cases.

## What This Repository Contains

- ATS and resume parsing workflows
- candidate screening and interview evaluation logic
- semantic matching and skill extraction modules
- reporting and demo generation pipelines
- documentation, validation reports, and roadmap materials

## Repository Structure

- [ats_engine](ats_engine/) – resume parsing and ATS-related analysis
- [screening_ai](screening_ai/) – screening and candidate evaluation logic
- [interview_ai](interview_ai/) – interview orchestration and analysis
- [scoring](scoring/) – scoring and ranking engines
- [skills](skills/) – skill extraction and normalization support
- [docs](docs/) – architecture, roadmap, reports, and portfolio docs
- [tests](tests/) – validation and regression test suite

## Setup Instructions

### Prerequisites

- Python 3.10 or newer
- pip
- Windows PowerShell, bash, or equivalent terminal

### Local Setup

1. Clone the repository.
2. Create and activate a virtual environment:
   - Windows PowerShell: `python -m venv .venv` then `.\.venv\Scripts\activate`
3. Install dependencies:
   - `pip install --upgrade pip`
   - `pip install -r requirements.txt`

### Run the Main Workflow

```bash
python main.py
```

### Demo and HR Interview Modules

The repository also includes demo and interview runners for stakeholder review:

```bash
python hr_interview/hr_interview_runner.py
python hr_scoring/hr_runner.py
python hr_interview/demo_runner.py
```

Generated outputs are written under the data folder, including HR interview and demo artifacts.

## Key Platform Capabilities

- semantic candidate-to-job matching
- skill extraction and normalization
- scoring for ATS, screening, and interview rounds
- structured reporting for hiring review
- reusable modules for future expansion

## Submission Package

This submission is organized for review and presentation:

- [docs/Final_Submission_Index.md](docs/Final_Submission_Index.md)
- [docs/Internship_Portfolio.md](docs/Internship_Portfolio.md)
- [docs/AI_Roadmap.md](docs/AI_Roadmap.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## License

This project is proprietary to Zecpath.

