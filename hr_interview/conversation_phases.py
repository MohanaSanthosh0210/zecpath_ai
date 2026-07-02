from hr_interview.interview_state import InterviewState


class ConversationPhases:

    """
    Controls the HR interview flow.
    """

    PHASES = [

        "INTRODUCTION",

        "CORE_HR",

        "ROLE_BASED",

        "CLOSING"

    ]

    def __init__(self):

        self.state = InterviewState()

    def start_interview(self):

        self.state.next_phase(

            "INTRODUCTION"

        )

        return {

            "phase":

                self.state.current_phase,

            "message":

                "Welcome! Let's begin with a brief introduction."

        }

    def move_to_core_hr(self):

        self.state.next_phase(

            "CORE_HR"

        )

        return {

            "phase":

                self.state.current_phase,

            "message":

                "Proceeding to the core HR interview."

        }

    def move_to_role_based(self):

        self.state.next_phase(

            "ROLE_BASED"

        )

        return {

            "phase":

                self.state.current_phase,

            "message":

                "Proceeding to role-specific questions."

        }

    def move_to_closing(self):

        self.state.next_phase(

            "CLOSING"

        )

        self.state.end_interview()

        return {

            "phase":

                self.state.current_phase,

            "message":

                "Interview completed. Thank you."

        }

    def capture_response(

        self,

        question_id,

        question,

        response

    ):

        response = response.strip()

        follow_up = False

        if len(response.split()) < 5:

            follow_up = True

        self.state.update(

            question_id,

            question,

            response,

            follow_up

        )

        return {

            "question_id":

                question_id,

            "follow_up_required":

                follow_up,

            "current_phase":

                self.state.current_phase

        }


if __name__ == "__main__":

    interview = ConversationPhases()

    print(interview.start_interview())

    print()

    print(

        interview.capture_response(

            "INTRO_001",

            "Tell me about yourself.",

            "I am a software engineer."

        )

    )

    print()

    print(

        interview.move_to_core_hr()

    )

    print()

    print(

        interview.move_to_role_based()

    )

    print()

    print(

        interview.move_to_closing()

    )

    print()

    print(interview.state.to_dict())