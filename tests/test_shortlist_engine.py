from scoring.shortlist_engine import classify_candidate


def test_shortlisted():

    assert classify_candidate(85) == "Shortlisted"


def test_review():

    assert classify_candidate(55) == "Review"


def test_rejected():

    assert classify_candidate(20) == "Rejected"