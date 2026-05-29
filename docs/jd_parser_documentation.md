# Job Description Parsing Documentation

## Objective

Convert raw employer job descriptions into structured AI-readable objects.

---

# Features

- Extract job titles
- Extract required skills
- Extract education requirements
- Extract experience requirements
- Normalize JD text
- Create structured JSON outputs

---

# Modules

## jd_parser.py

Responsible for extracting structured entities from JD text.

## jd_cleaner.py

Cleans formatting issues and normalizes text.

## jd_extractor.py

Processes all job descriptions and generates structured JSON outputs.

---

# Output Structure

Each JD is converted into:

- Job Title
- Skills
- Experience
- Education

---

# Benefits

- AI-ready job profiles
- ATS compatibility
- Better candidate matching
- Standardized job data