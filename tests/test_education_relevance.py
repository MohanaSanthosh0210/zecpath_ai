from scoring.education_relevance import calculate_education_score


def test_calculate_education_score_exact_match():
    assert calculate_education_score("Computer Science", "Computer Science") == 100


def test_calculate_education_score_related_fields():
    assert calculate_education_score("Computer Science", "Software Engineering") == 80


def test_calculate_education_score_field_substring():
    assert calculate_education_score("Supply Chain", "Logistics") == 80


def test_calculate_education_score_degree_bonus():
    score = calculate_education_score(
        "Computer Science",
        "Software Engineering",
        candidate_degree="Master's Degree",
        required_degree="Bachelor's Degree",
    )
    assert score == 85