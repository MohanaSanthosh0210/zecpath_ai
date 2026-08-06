# Scoring Logic Overview

This document summarizes the scoring components used across the platform and points to the implementation locations.

Core scoring engines
- Technical Scoring: implemented in `technical_scoring/technical_scoring_engine.py` and supporting scorers in the `technical_scoring/` package. See [technical_scoring/technical_scoring_engine.py](technical_scoring/technical_scoring_engine.py) for the evaluator entrypoint.
- HR Interview Scoring: implemented in `hr_scoring/hr_scoring_engine.py`. See [hr_scoring/hr_scoring_engine.py](hr_scoring/hr_scoring_engine.py).
- Unified Scoring: combines ATS, screening, and HR signals in `scoring/unified_scoring_engine.py`. See [scoring/unified_scoring_engine.py](scoring/unified_scoring_engine.py).

Weight configuration and rubrics
- Weights and rubrics are loaded via `technical_scoring/rubric_loader.py` and `hr_scoring/weight_config.py` (where present). Maintain these files to tune behavior.

Processing pipeline
- Individual scorers compute dimension-specific scores (accuracy, depth, reasoning, applicability, communication, confidence).
- Scores are combined with configurable weights to produce a weighted score.
- Difficulty normalizers adjust raw scores based on question difficulty.
- The `UnifiedScoringEngine` maps role-based weight presets (`schemas/scoring_weights.py`) and emits a unified hiring fit percentage and status.

Where to update logic
- To change scoring behavior, update the specific scorer module (e.g., `technical_scoring/accuracy_scorer.py`) and the corresponding rubric/weights loader.

Quick example

See [scoring/unified_scoring_engine.py](scoring/unified_scoring_engine.py) for the canonical `calculate` interface.
