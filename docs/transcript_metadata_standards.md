# Transcript Metadata Standards

## Candidate Identification

Each transcript must contain:

- candidate_id
- job_id
- transcript_id

## Question Mapping

Every response must be linked to:

- question_id

This allows answer-level scoring.

## Confidence Level

Range:

0.0 - 1.0

Examples:

1.00 = Perfect recognition

0.95 = High confidence

0.80 = Medium confidence

Below 0.70 = Review required

## Timestamp Format

HH:MM:SS

Example:

00:01:32

## Language Codes

en = English

hi = Hindi

ml = Malayalam

ta = Tamil

## Normalization Rules

Convert text to lowercase

Remove filler words:

- um
- uh
- like
- you know

Normalize spacing

Remove duplicate punctuation

Convert speech numbers:

three years

→

3 years

Standardize dates

Example:

June 3rd 2026

→

2026-06-03