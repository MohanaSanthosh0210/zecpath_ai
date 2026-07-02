from hr_interview.interview_categories import InterviewCategories


class RoleBasedQuestionGenerator:

    """
    Generates HR interview questions
    based on candidate profile.
    """

    FRESHER_QUESTIONS = [

        {
            "id": "FRESHER_001",
            "question": "Tell me about your final year project."
        },

        {
            "id": "FRESHER_002",
            "question": "Why should we hire you as a fresher?"
        }

    ]

    EXPERIENCED_QUESTIONS = [

        {
            "id": "EXP_001",
            "question": "Tell me about your most recent role."
        },

        {
            "id": "EXP_002",
            "question": "What was your biggest professional achievement?"
        }

    ]

    TECHNICAL_QUESTIONS = [

        {
            "id": "TECH_001",
            "question": "Explain a technically challenging project you worked on."
        },

        {
            "id": "TECH_002",
            "question": "How do you keep your technical skills up to date?"
        }

    ]

    NON_TECHNICAL_QUESTIONS = [

        {
            "id": "NONTECH_001",
            "question": "How do you prioritize multiple responsibilities?"
        },

        {
            "id": "NONTECH_002",
            "question": "Describe a situation where you handled a difficult customer or stakeholder."
        }

    ]

    def generate_questions(

        self,

        experience_level,

        role_type

    ):

        questions = []

        # ----------------------------------
        # Common HR Questions
        # ----------------------------------

        for category in InterviewCategories.get_categories().values():

            questions.extend(category)

        # ----------------------------------
        # Experience Level
        # ----------------------------------

        if experience_level.lower() == "fresher":

            questions.extend(

                self.FRESHER_QUESTIONS

            )

        else:

            questions.extend(

                self.EXPERIENCED_QUESTIONS

            )

        # ----------------------------------
        # Role Type
        # ----------------------------------

        if role_type.lower() == "technical":

            questions.extend(

                self.TECHNICAL_QUESTIONS

            )

        else:

            questions.extend(

                self.NON_TECHNICAL_QUESTIONS

            )

        return questions


if __name__ == "__main__":

    generator = RoleBasedQuestionGenerator()

    questions = generator.generate_questions(

        experience_level="Experienced",

        role_type="Technical"

    )

    print("\n========== GENERATED HR QUESTIONS ==========\n")

    for question in questions:

        print(

            f"{question['id']} : {question['question']}"

        )