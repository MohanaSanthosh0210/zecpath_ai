class SkillExtractor:

    SKILLS = [

        "python",
        "java",
        "c++",
        "django",
        "flask",
        "fastapi",
        "react",
        "nodejs",
        "mysql",
        "mongodb",
        "aws",
        "docker",
        "git",
        "machine learning",
        "tensorflow",
        "pytorch"
    ]

    @staticmethod
    def extract(answer):

        answer = answer.lower()

        return [

            skill

            for skill in SkillExtractor.SKILLS

            if skill in answer
        ]