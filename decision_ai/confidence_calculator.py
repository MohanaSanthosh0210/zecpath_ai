class ConfidenceCalculator:

    @staticmethod
    def calculate(

        hiring_fit,

        integrity_score,

        behavior_score

    ):

        confidence = (

            hiring_fit * 0.50 +

            integrity_score * 0.30 +

            behavior_score * 0.20

        )

        return round(confidence, 2)