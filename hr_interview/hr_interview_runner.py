from hr_interview.interview_flow import InterviewFlow


def main():

    flow = InterviewFlow()

    flow.save(

        experience_level="Experienced",

        role_type="Technical"

    )


if __name__ == "__main__":

    main()