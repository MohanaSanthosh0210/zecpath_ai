# Performance Report

## Overview

This report documents the optimization and stability improvements applied to the ATS pipeline, with benchmark results from processing four sample resumes.

## Resume Parsing

- DOCX read time: 0.0218 sec
- PDF read time range: 0.1212–0.3287 sec
- Average read time: 0.1869 sec

## Skill Extraction

- Average skill extraction time: 0.0466 sec
- Improved noisy text handling and regex compilation reduced repeated work and lowered latency.

## Education Parsing

- Average education parsing time: 0.0018 sec
- Added raw-text education parsing support for direct resume text input.

## Experience Parsing

- Average experience parsing time: 0.0005 sec
- Added stable experience section detection and fallback parsing for noisy resumes.

## Total ATS Runtime

- Average complete pipeline time: 0.2357 sec
- Sample count: 4 resumes

## Sample Results

- `resume1.docx`: 0.0428 sec total
- `resume1.pdf`: 0.3851 sec total
- `resume2.pdf`: 0.3549 sec total
- `resume3.pdf`: 0.1602 sec total

## Optimizations Applied

- Added a universal `DocumentReader` for PDF and DOCX extraction
- Created `EducationParser` wrapper and raw-text education extraction support
- Compiled key regex patterns once during initialization
- Added fuzzy-match caching to reduce repeated string comparisons
- Applied text normalization and noise filtering to improve entity detection
- Kept memory use low with lightweight parsing and explicit garbage collection
- Stabilized resume processing for noisy or malformed documents