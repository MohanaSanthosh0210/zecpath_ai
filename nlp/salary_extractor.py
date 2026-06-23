import re


class SalaryExtractor:

    @staticmethod
    def extract(answer):

        match = re.search(

            r'(\d+)\s*lpa',

            answer.lower()
        )

        if match:
            return f"{match.group(1)} LPA"

        return None