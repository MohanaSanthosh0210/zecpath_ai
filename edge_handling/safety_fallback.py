class SafetyFallback:

    @staticmethod
    def execute(reason):

        return {

            "action":

                "Move candidate to recruiter review",

            "reason":

                reason,

            "status":

                "Fallback"

        }