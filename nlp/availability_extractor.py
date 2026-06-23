import re


class AvailabilityExtractor:

    @staticmethod
    def extract(answer):

        answer = answer.lower()

        if "immediately" in answer:
            return "Immediately"

        match = re.search(

            r'(\d+)\s*(day|days|month|months)',

            answer
        )

        if match:
            return match.group(0)

        return None