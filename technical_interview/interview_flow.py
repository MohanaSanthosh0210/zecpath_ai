class InterviewFlow:

    STATES = [

        "INTRODUCTION",

        "EXPERIENCE_DISCUSSION",

        "CONCEPTUAL_QUESTIONS",

        "PRACTICAL_QUESTIONS",

        "SCENARIO_BASED",

        "TECHNICAL_EVALUATION",

        "SUMMARY",

        "END"

    ]

    @staticmethod
    def next_state(current_state):

        if current_state not in InterviewFlow.STATES:

            return "END"

        index = InterviewFlow.STATES.index(current_state)

        if index == len(InterviewFlow.STATES) - 1:

            return "END"

        return InterviewFlow.STATES[index + 1]