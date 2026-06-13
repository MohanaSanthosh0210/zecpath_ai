# Zecpath ATS Developer Guide

## Project Structure

parsers/
skills/
scoring/
tests/
data/

---

## Running Resume Parsing

python parsers/resume_parser.py

---

## Running Skill Extraction

python skills/skill_extractor.py

---

## Running ATS Scoring

python scoring/ats_scoring_runner.py

---

## Running Candidate Ranking

python scoring/ranking_runner.py

---

## Running Fairness Evaluation

python scoring/fairness/fairness_runner.py

---

## Running Performance Benchmark

python -m tests.test_performance

---

## Troubleshooting

### Module Not Found

Solution:

Run from project root:

python -m module_name

---

### SpaCy Errors

Install:

pip install spacy

Verify:

python -c "import spacy"

---

### Torch DLL Error

Reinstall CPU version:

pip uninstall torch torchvision torchaudio

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

---

### Missing Dependencies

pip install -r requirements.txt

---

## Future Extensions

* LLM Resume Understanding
* Interview Intelligence Engine
* Candidate Behaviour Analysis
* AI Hiring Assistant
* Recruiter Copilot
