from parsers.education_parser import extract_education


def test_extract_education_entries_from_resume():
    data = {
        "education": [
            "Dec 2020 May 2022 Masters Degree in Human Computer Interaction (HCI), Pratt Institute Jul 2016 Nov 2020 Bachelors Degree in Interaction Design, Pratt Institute New York - Excelled in Usability Testing coursework."
        ],
        "certifications": [
            "Certified Head Nutrition Consultant , Food Sciences Council Jul 2021 Jul 2021 ACCOMPLISHMENTS - Decreased TPN usage through nutrition support team by 72."
        ],
    }
    profile = extract_education(data)
    assert len(profile["education"]) == 2
    assert profile["education"][0]["degree_type"] == "Master's Degree"
    assert profile["education"][0]["field_of_study"] == "Human Computer Interaction"
    assert profile["education"][0]["institution"] == "Pratt Institute"
    assert profile["education"][0]["graduation_year"] == "2022"
    assert profile["certifications"]
    assert profile["certifications"][0]["category"] == "Healthcare"