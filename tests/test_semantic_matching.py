from scoring.semantic_matching import SemanticMatchingEngine


def test_semantic_matching_scores_relevant_resume_highly():
    resume_profile = {
        "skills": ["Python", "AWS", "Kubernetes"],
        "experience": [
            {
                "designation": "Senior Software Engineer",
                "responsibilities": [
                    "Built and deployed cloud-native applications with Python and AWS.",
                    "Managed Kubernetes clusters for production services.",
                ],
            }
        ],
        "projects": [
            {
                "description": "Migrated monolith to AWS ECS, added CI/CD pipelines, and reduced deployment time by 60%."
            }
        ],
    }

    job_profile = {
        "job_title": "Senior Cloud Engineer",
        "job_description": "Seeking an experienced engineer with strong Python, AWS, and Kubernetes experience to operate cloud infrastructure.",
        "required_skills": ["Python", "AWS", "Kubernetes"],
        "projects": [
            {
                "description": "Lead the migration of legacy systems to cloud infrastructure and improve deployment automation."
            }
        ],
    }

    engine = SemanticMatchingEngine()
    score = engine.score_pair(resume_profile, job_profile)

    assert score["skills_similarity"] >= 0.7
    assert score["experience_similarity"] >= 0.2
    assert score["project_similarity"] >= 0.02
    assert score["overall_similarity"] >= 0.45
    assert score["match"] is True


def test_semantic_matching_tunes_thresholds_with_labels():
    engine = SemanticMatchingEngine(thresholds={"skills": 0.5, "experience": 0.4, "projects": 0.3, "overall": 0.5})

    positive_pair = (
        {
            "skills": ["Python", "Django", "AWS"],
            "experience": [
                {
                    "designation": "Backend Engineer",
                    "responsibilities": [
                        "Developed REST APIs using Django and deployed services to AWS."
                    ],
                }
            ],
            "projects": ["API development and AWS deployment"],
        },
        {
            "job_title": "Backend Developer",
            "job_description": "Build REST APIs with Python and Django, deploy to AWS.",
            "required_skills": ["Python", "Django", "AWS"],
            "projects": ["REST API development"],
        },
        True,
    )

    negative_pair = (
        {
            "skills": ["Graphic Design", "Photoshop"],
            "experience": [
                {
                    "designation": "Graphic Designer",
                    "responsibilities": [
                        "Created visual assets and branding materials using Photoshop."],
                }
            ],
            "projects": ["Brand identity refresh"],
        },
        {
            "job_title": "Backend Developer",
            "job_description": "Build REST APIs with Python and Django, deploy to AWS.",
            "required_skills": ["Python", "Django", "AWS"],
            "projects": ["REST API development"],
        },
        False,
    )

    tuned = engine.tune_thresholds([positive_pair, negative_pair])
    assert 0.2 < tuned["overall"] < 0.9
    assert engine.thresholds["overall"] == tuned["overall"]