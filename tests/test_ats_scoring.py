import os
import sys

sys.path.append(
    os.path.abspath(".")
)

from scoring.ats_scoring_engine import calculate_ats_score

score = calculate_ats_score(

    role="python developer",

    skill_score=90,

    experience_score=85,

    education_score=80,

    semantic_score=88
)

print("ATS Score =", score)