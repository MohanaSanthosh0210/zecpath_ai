import re


def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    return " ".join(
        text.split()
    )


def normalize_skills(skills):

    normalized = []

    for skill in skills:

        if isinstance(skill, dict):

            skill = skill.get(
                "name",
                ""
            )

        normalized.append(
            normalize_text(
                str(skill)
            )
        )

    return list(
        set(normalized)
    )


def normalize_resume(resume):

    return {

        "skills":
        normalize_skills(
            resume.get(
                "skills",
                []
            )
        ),

        "experience":
        resume.get(
            "experience",
            []
        ),

        "education":
        resume.get(
            "education_sections",
            []
        ),

        "projects":
        resume.get(
            "projects",
            []
        )
    }