class ClarityAnalyzer:
    """
    Evaluates how clearly a candidate explains an answer.

    The score is based on:

    • Number of complete sentences
    • Average sentence length
    • Logical connectors
    • Explanation completeness

    Output:
        clarity_score (0–100)
    """

    CONNECTORS = [

        "because",

        "therefore",

        "however",

        "for example",

        "for instance",

        "first",

        "second",

        "finally",

        "then",

        "next",

        "after",

        "also",

        "so",

        "thus"

    ]

    @classmethod
    def analyze(cls, answer):

        answer = answer.strip()

        sentences = [

            s.strip()

            for s in answer.replace("!", ".").replace("?", ".").split(".")

            if s.strip()

        ]

        sentence_count = len(sentences)

        words = answer.split()

        word_count = len(words)

        avg_sentence_length = (

            word_count / sentence_count

            if sentence_count > 0

            else 0

        )

        connector_count = 0

        lower = answer.lower()

        for connector in cls.CONNECTORS:

            if connector in lower:

                connector_count += 1

        score = 50

        # Multiple complete sentences

        if sentence_count >= 2:

            score += 20

        # Enough explanation

        if word_count >= 12:

            score += 15

        # Good sentence length

        if avg_sentence_length >= 6:

            score += 10

        # Logical connectors

        score += connector_count * 5

        score = min(100, score)

        return {

            "clarity_score": score,

            "sentence_count": sentence_count,

            "average_sentence_length":

                round(

                    avg_sentence_length,

                    2

                ),

            "connectors_used": connector_count

        }


if __name__ == "__main__":

    sample = (

        "I have two years of experience in Python. "

        "I worked on Flask and Django projects."

    )

    print(

        ClarityAnalyzer.analyze(

            sample

        )

    )