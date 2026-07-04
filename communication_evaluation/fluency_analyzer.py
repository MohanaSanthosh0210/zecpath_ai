class FluencyAnalyzer:
    """
    Estimates fluency based on sentence continuity,
    average sentence length and filler words.
    """

    FILLER_WORDS = [
        "um",
        "uh",
        "hmm",
        "like",
        "you know",
        "actually",
        "basically"
    ]

    @classmethod
    def analyze(cls, answer):

        answer = answer.strip()

        words = answer.split()

        sentences = [
            s.strip()
            for s in answer.replace("?", ".").replace("!", ".").split(".")
            if s.strip()
        ]

        word_count = len(words)

        sentence_count = max(1, len(sentences))

        average_sentence_length = word_count / sentence_count

        filler_count = 0

        lower = answer.lower()

        for filler in cls.FILLER_WORDS:

            filler_count += lower.count(filler)

        score = 100

        score -= filler_count * 8

        if average_sentence_length < 6:
            score -= 15

        score = max(0, min(score, 100))

        return {

            "fluency_score": score,

            "sentence_count": sentence_count,

            "average_sentence_length":

                round(

                    average_sentence_length,

                    2

                ),

            "filler_count": filler_count

        }