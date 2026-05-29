import re

def extract_job_data(text):

    data = {
        "job_title": "",
        "skills": [],
        "experience": "",
        "education": ""
    }

    # Extract Job Title
    title_match = re.search(r"Job Title:(.*)", text)

    if title_match:
        data["job_title"] = title_match.group(1).strip()

    # Extract Skills
    skills = re.findall(
        r"Python|Machine Learning|FastAPI|Docker|SQL|Java",
        text,
        re.IGNORECASE
    )

    data["skills"] = list(set(skills))

    # Extract Experience
    exp_match = re.search(r"Experience:(.*)", text)

    if exp_match:
        data["experience"] = exp_match.group(1).strip()

    # Extract Education
    edu_match = re.search(r"Education:(.*)", text)

    if edu_match:
        data["education"] = edu_match.group(1).strip()

    return data