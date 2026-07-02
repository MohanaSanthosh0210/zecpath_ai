from hr_interview.role_based_question_generator import (
    RoleBasedQuestionGenerator
)


class QuestionBank:

    """
    Stores and retrieves interview questions.
    """

    def __init__(self):

        self.generator = RoleBasedQuestionGenerator()

    def build_question_bank(

        self,

        experience_level,

        role_type

    ):

        return self.generator.generate_questions(

            experience_level,

            role_type

        )

    def total_questions(

        self,

        experience_level,

        role_type

    ):

        return len(

            self.build_question_bank(

                experience_level,

                role_type

            )

        )