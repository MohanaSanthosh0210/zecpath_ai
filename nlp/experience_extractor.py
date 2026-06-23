import re


class ExperienceExtractor:

    @staticmethod
    def extract(answer):

        match = re.search(

            r'(\d+)\s*(year|years|month|months)',

            answer.lower()
        )

        if not match:
            return None

        return match.group(0)