class InterviewCategories:

    """
    Defines all HR interview categories and
    the default questions for each category.
    """

    CATEGORIES = {

        "self_introduction": [

            {
                "id": "INTRO_001",
                "question": "Tell me about yourself."
            }

        ],

        "career_journey": [

            {
                "id": "CAREER_001",
                "question": "Can you describe your career journey so far?"
            }

        ],

        "strengths_weaknesses": [

            {
                "id": "SW_001",
                "question": "What are your greatest strengths?"
            },

            {
                "id": "SW_002",
                "question": "What is one weakness you are currently improving?"
            }

        ],

        "teamwork_culture_fit": [

            {
                "id": "TEAM_001",
                "question": "Describe a time you worked successfully in a team."
            },

            {
                "id": "TEAM_002",
                "question": "How do you handle disagreements with teammates?"
            }

        ],

        "career_goals": [

            {
                "id": "GOAL_001",
                "question": "Where do you see yourself in the next five years?"
            }

        ],

        "availability_commitment": [

            {
                "id": "AVAIL_001",
                "question": "When can you join our organization?"
            },

            {
                "id": "AVAIL_002",
                "question": "Are you open to relocation if required?"
            }

        ]

    }

    @classmethod
    def get_categories(cls):

        return cls.CATEGORIES

    @classmethod
    def get_questions(cls, category):

        return cls.CATEGORIES.get(category, [])