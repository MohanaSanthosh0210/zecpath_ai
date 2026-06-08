"""
Day 14 - Shortlisting Automation
"""


SHORTLIST_THRESHOLD = 70
REVIEW_THRESHOLD = 50


def classify_candidate(score: float) -> str:
    """
    Categorize candidate
    """

    if score >= SHORTLIST_THRESHOLD:
        return "Shortlisted"

    elif score >= REVIEW_THRESHOLD:
        return "Review"

    return "Rejected"