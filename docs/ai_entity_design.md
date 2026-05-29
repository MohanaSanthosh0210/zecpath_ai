# AI Data Entity Design Document

## 1. Overview
This document defines the standardized data architecture for the Zecpath AI platform. The goal is to transform unstructured hiring inputs—specifically resumes and job descriptions—into clean, machine-readable JSON entities. This structure enables the AI engine to perform high-accuracy screening, automated ranking, and matching.

## 2. Core Data Entities

* **Candidate Profile**: The unified record for an applicant. Contains personal info, skills, experience history, education, and certifications.
* **Job Profile**: The template for defining role requirements, including job title, industry, skill requirements, and experience range.
* **Skill Object**: A modular unit representing competency with `name`, `proficiency`, and `years_experience`.
* **Experience Object**: A standardized block capturing `company`, `designation`, `duration`, and `responsibilities`.

## 3. Design Logic
* **Extensibility**: The schema uses arrays (e.g., for `skills`, `experience`, `education`) to ensure the model scales gracefully for all professional levels.
* **Standardization**: By enforcing consistent data types (e.g., `number` for years/dates, `string` for text), the ranking engine can calculate compatibility scores programmatically.
* **Decision Support**: Standardized entities allow the system to persist the AI's "reasoning" for a candidate's score, which is critical for future auditing and model training.

## 4. Relationship Summary
The matching engine evaluates a **Candidate Profile** against a **Job Profile** by comparing the values within their respective **Skill** and **Experience** objects to generate a compatibility score.