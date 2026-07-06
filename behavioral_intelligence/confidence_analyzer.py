class ConfidenceAnalyzer:
    """
    Detects hesitation patterns and estimates
    candidate confidence.
    """

    UNCERTAINTY_PHRASES = [

        "i think",

        "maybe",

        "perhaps",

        "probably",

        "not sure",

        "kind of",

        "sort of",

        "i guess",

        "i believe"

    ]

    @staticmethod
    def analyze(answer: str):

        answer = answer.lower()

        hesitation_count = 0

        detected = {}

        for phrase in ConfidenceAnalyzer.UNCERTAINTY_PHRASES:

            count = answer.count(phrase)

            if count > 0:

                detected[phrase] = count

                hesitation_count += count

        words = answer.split()

        repeated_words = 0

        repeated_list = []

        for i in range(1, len(words)):

            if words[i] == words[i - 1]:

                repeated_words += 1

                repeated_list.append(words[i])

        confidence_score = max(

            0,

            100 - (

                hesitation_count * 10 +

                repeated_words * 5

            )

        )

        return {

            "confidence_score": confidence_score,

            "hesitation_count": hesitation_count,

            "repeated_words": repeated_words,

            "detected_hesitations": detected,

            "repeated_word_list": repeated_list

        }


if __name__ == "__main__":

    sample = (

        "I think maybe I can work "

        "work on Django."

    )

    print(

        ConfidenceAnalyzer.analyze(

            sample

        )

    )