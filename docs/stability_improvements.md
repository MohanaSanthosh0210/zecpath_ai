# Stability Improvements

## Error Handling

Added try-except blocks to:
- PDF parser
- DOCX parser

## Logging

Errors logged using logger.py

## Missing Data Handling

Null scores converted to 0

## Resume Cleaning

Improved noisy resume processing
- Added non-ASCII noise filtering and normalized whitespace before extraction.

## Entity Detection

Case-insensitive education and experience detection
- Expanded context patterns for skills, tools, and framework listings.

## Memory Optimization

Unused objects released after processing
- Added fuzzy-match caching and reduced repeated regex compilation.

## Parser Stability

- Added a universal `DocumentReader` for both PDF and DOCX input.
- Added `EducationParser` to support raw resume text extraction and avoid import mismatches.