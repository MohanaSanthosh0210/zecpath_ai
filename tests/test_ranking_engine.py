from scoring.ranking_engine import rank_candidates


def test_rank_candidates():

    candidates = [
        {
            "candidate_id": "c1",
            "final_ats_score": 55
        },
        {
            "candidate_id": "c2",
            "final_ats_score": 90
        },
        {
            "candidate_id": "c3",
            "final_ats_score": 70
        }
    ]

    ranked = rank_candidates(
        candidates
    )

    assert ranked[0]["final_ats_score"] == 90
    assert ranked[1]["final_ats_score"] == 70
    assert ranked[2]["final_ats_score"] == 55

    assert ranked[0]["rank"] == 1