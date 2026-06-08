"""
Day 14 - Candidate Ranking Engine

Responsible for:
- Sorting candidates by ATS score
- Assigning ranks
"""

from typing import List, Dict


def rank_candidates(candidates: List[Dict]) -> List[Dict]:
    """
    Sort candidates by ATS score descending
    """

    ranked = sorted(
        candidates,
        key=lambda x: x.get("final_ats_score", 0),
        reverse=True
    )

    for rank, candidate in enumerate(ranked, start=1):
        candidate["rank"] = rank

    return ranked