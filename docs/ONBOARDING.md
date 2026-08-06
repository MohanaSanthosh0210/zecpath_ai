# Developer Onboarding Guide

This guide helps a new developer get the project running locally and find core modules quickly.

1) Clone and install

```bash
git clone <repo-url>
cd zecpath-ai-platform
python -m venv .venv
\.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

2) Run quick smoke test

```bash
python main.py
# or run a few unit tests
pytest -q tests/test_observability.py
```

3) Code layout (quick tour)

- `main.py` — local entrypoint for batch runs and examples.
- `adaptive_followup/` — follow-up question and conversation adaptation logic.
- `technical_scoring/` — technical answer scorers and rubric loader.
- `hr_scoring/`, `scoring/` — HR interview scoring and unified scoring aggregation.
- `communication_evaluation/`, `behavior_analysis/` — modules for communication and behavioral signals.
- `schemas/` — schema and config definitions.
- `docs/` — technical documentation (start here).

4) Running and debugging

- Use your IDE to open the workspace and set breakpoints in the module of interest.
- Many components can be exercised by creating sample JSON inputs under `data/examples/` and running their engines directly (e.g., `python hr_scoring/hr_scoring_engine.py`).

5) Tests & linting

- Run unit tests: `pytest -q`.
- Add tests under `tests/` when modifying behavior.

6) How to contribute

- Create a feature branch, open a pull request, and include unit tests and docs updates.
- Update this onboarding doc when adding new top-level components.
